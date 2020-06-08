from django.shortcuts import render, reverse, redirect
from django.views import View
from django import http
from django.db import DatabaseError
from django.contrib.auth import login, authenticate, logout
from django_redis import get_redis_connection
from django.contrib.auth.mixins import LoginRequiredMixin
import re, json, logging

from users.models import User, Address
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.views import LoginRequiredJSONMixin
from celery_tasks.email.tasks import send_verify_email
from users.utils import generate_verify_email_url, check_verify_email_token
from . import constants
from goods.models import SKU
# Create your views here.

logger = logging.getLogger('django')


class UserBrowseHistory(LoginRequiredJSONMixin, View):
    """用戶瀏覽紀錄"""

    def post(self, request):
        """保存用戶商品瀏覽紀錄"""
        # 接收參數
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        sku_id = json_dict.get('sku_id')

        # 校驗參數
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('參數sku_id錯誤')

        # 保存sku_id到redis
        redis_conn = get_redis_connection('history')
        user = request.user
        pl = redis_conn.pipeline()
        # 先去重
        pl.lrem('history_%s' % user.id, 0, sku_id)
        # 再保存:最近瀏覽的商品在最前面
        pl.lpush('history_%s' % user.id, sku_id)
        # 最後擷取
        pl.ltrim('history_%s' % user.id, 0, 4)
        # 執行
        pl.execute()

        # 響應結果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

        pass


class UpdateTitleAddressView(LoginRequiredJSONMixin, View):
    """修改收貨地址標題"""

    def put(self, request, address_id):

        # 接收參數
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        if not title:
            return http.HttpResponseForbidden('缺少title')

        try:
            address = Address.objects.get(id=address_id)
            address.title = title
            address.save()

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新標題失敗'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '更新標題成功'})


class DefaultAddressView(LoginRequiredJSONMixin, View):
    """設置默認收貨地址"""

    def put(self, request, address_id):

        try:
            address = Address.objects.get(id=address_id)

            request.user.default_address = address
            request.user.save()

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '設置默認地址失敗'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '設置默認地址成功'})


class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):
    """修改與刪除收貨地址"""

    def put(self, request, address_id):
        """修改地址"""

        # 接收參數
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校驗參數
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必傳參數')
        if not re.match(r'^09\d{8}$', mobile):
            return http.HttpResponseForbidden('手機號碼有誤')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('固定電話有誤')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('email有誤')

        # 判斷地址是否存在並更新地址
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新地址失敗'})

        # 構造響應數據
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '更新地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        """刪除地址"""

        try:
            address = Address.objects.get(id=address_id)
            address.is_deleted = True
            address.save()

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '刪除地址失敗'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '刪除地址成功'})


class AddressCreateView(LoginRequiredJSONMixin, View):
    """新增用戶地址"""
    def post(self, request):

        # 判斷用戶地址數量是否超過上限
        count = request.user.addresses.count()  # 一查多,使用related_name來查
        if count > constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超出用戶地址上限'})

        # 接收參數
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校驗參數
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必傳參數')
        if not re.match(r'09\d{8}$', mobile):
            return http.HttpResponseForbidden('手機號碼有誤')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('固定電話有誤')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('email有誤')

        # 保存用戶傳入的地址
        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )

            # 如果用戶沒有默認地址,需指定默認地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失敗'})

        # 構造新增地址字典
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address_dict})


class AddressView(LoginRequiredMixin, View):
    """用戶收貨地址"""

    def get(self, request):
        """查詢並展示用戶地址訊息"""

        # 獲取當前登入用戶
        login_user = request.user

        # 查詢地址
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        # 將用戶地址模型列表,轉成字典列表:因為JsonResponse和Vue.js不認識模型類,只有Django和Jinja2模板引擎認識
        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)

        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_dict_list,
        }

        return render(request, 'user_center_site.html', context)


class VerifyEmailView(View):
    """驗證郵箱"""

    def get(self, request):
        token = request.GET.get('token')

        # 校驗參數
        if not token:
            return http.HttpResponseForbidden('缺少token')

        # 從token中提取用戶訊息
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseBadRequest('無效的token')

        # 將用戶的email_active欄位設為true
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活郵箱失敗')

        return redirect(reverse('users:info'))


class EmailView(LoginRequiredJSONMixin, View):
    """添加郵箱"""

    def put(self, request):
        # 接收參數
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')

        # 校驗參數
        if not email:
            return http.HttpResponseForbidden('缺少email參數')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('參數email有誤')

        # 將用戶傳入的email保存到用戶表的email欄位
        try:
            request.user.email = email
            request.user.save()

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增郵箱失敗'})

        # 發送驗證郵件
        verify_url = generate_verify_email_url(request.user)
        send_verify_email.delay(email, verify_url)

        # 響應結果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class UserInfoView(LoginRequiredMixin, View):
    """用戶中心"""

    def get(self, request):
        """提供用戶中心頁面"""
        # 如果LoginRequiredMixin判斷出用戶已登入,那麼request.user就是登入用戶對象
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        return render(request, 'user_center_info.html', context)


class LogoutView(View):

    def get(self, request):

        logout(request)

        response = redirect(reverse('contents:index'))

        response.delete_cookie('username')

        return response


class LoginView(View):
    """用戶登入"""

    def get(self, request):
        """提供用戶登入頁面"""

        return render(request, 'login.html')

    def post(self, request):
        """用戶登入邏輯"""

        # 接收參數
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 校驗參數
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必傳參數')

        if not re.match(r'^[a-zA-z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('請輸入正確的用戶名')

        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('密碼最少8位,最長20位')

        # 認證用戶
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '帳號或密碼錯誤'})

        # 狀態保持
        login(request, user)
        # 使用remembered來確定狀態保持週期(實現記住登入)
        if remembered != 'on':
            # 沒有記住登入,狀態保持在瀏覽器繪畫結束後就銷毀
            request.session.set_expiry(0)  # 單位是秒
        else:
            # 記住登入,狀態保持週期為兩周,None預設為兩周
            request.session.set_expiry(None)

        # 先取出next
        next = request.GET.get('next')
        if next:
            # 重定向到next所指的頁面
            response = redirect(next)
        else:
            # 重定向到首頁
            response = redirect(reverse('contents:index'))

        # 為了在首頁右上角顯示用戶名,須將用戶名緩存到cookie中
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        return response


class UsernameCountView(View):
    """判斷用戶是否重複註冊"""

    def get(self, request, username):

        count = User.objects.filter(username=username).count()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):
    """判斷用戶手機是否重複"""

    def get(self, request, mobile):

        count = User.objects.filter(mobile=mobile).count()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class RegisterView(View):
    """用戶註冊"""

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        allow = request.POST.get('allow')

        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden("缺少必傳參數");

        if not re.match(r'^[0-9a-zA-Z_-]{5,20}$', username):
            return http.HttpResponseForbidden("請輸入5-20位字符的用戶名");

        if not re.match(r'^[0-9a-zA-Z_-]{8,20}$', password):
            return http.HttpResponseForbidden("請輸入8-20位密碼");

        if password != password2:
            return http.HttpResponseForbidden("兩次輸入的密碼不一致");

        if not re.match(r'^09\d{8}$', mobile):
            return http.HttpResponseForbidden("手機格式有誤");

        # 判斷簡訊驗證碼是否正確
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '簡訊驗證碼已失效'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'register.html', {'sms_code_errmsg': '輸入簡訊驗證碼有誤'})

        if allow != 'on':
            return http.HttpResponseForbidden("請勾選用戶協議");

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)

        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '註冊失敗'})

        # 登入狀態保持
        login(request, user)

        # 響應,重定向到首頁
        response = redirect(reverse('contents:index'))

        # 為了在首頁右上角顯示用戶名,須將用戶名緩存到cookie中
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        return response

