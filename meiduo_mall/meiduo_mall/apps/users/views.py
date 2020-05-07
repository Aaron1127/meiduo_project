from django.shortcuts import render, reverse, redirect
from django.views import View
from django import http
from django.db import DatabaseError
from django.contrib.auth import login, authenticate, logout
from django_redis import get_redis_connection
from django.contrib.auth.mixins import LoginRequiredMixin
import re

from users.models import User
from meiduo_mall.utils.response_code import RETCODE
# Create your views here.


class UserInfoView(LoginRequiredMixin, View):
    """用戶中心"""

    def get(self, request):

        return render(request, 'user_center_info.html')


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

