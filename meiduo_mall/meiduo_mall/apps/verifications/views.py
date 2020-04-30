from django.shortcuts import render
from django.views import View

from verifications.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http
from . import constants
from meiduo_mall.utils.response_code import RETCODE
import random

# Create your views here.


class SMSCodeView(View):
    """簡訊驗證碼"""

    def get(self, request, mobile):
        """
        :param request:
        :param mobile: 手機號碼
        :return: JSON
        """
        # 接收參數
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        # 校驗參數
        if not all([mobile, image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必傳參數')

        # 提取圖形驗證碼
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_%s' % uuid)

        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '圖形驗證碼已失效'})

        # 刪除圖形驗證碼
        redis_conn.delete('img_%s' % uuid)

        # 對比圖形驗證碼
        image_code_server = image_code_server.decode()  # 將byte轉成字符串
        if image_code_client.lower() != image_code_server.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '輸入的圖形驗證碼有誤'})

        # 生成簡訊驗證碼
        # sms_code = '%06d' % random.randint(0, 999999)
        sms_code = '123456'

        # 保存簡訊驗證碼
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 發送簡訊驗證碼
        # TO DO

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '發送簡訊成功'})




class ImageCodeView(View):

    def get(self, request, uuid):

        # 生成圖形驗證碼
        text, image = captcha.generate_captcha()

        # 保存圖形驗證碼
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 返回圖形驗證碼
        return http.HttpResponse(image, content_type='image/jpg')
