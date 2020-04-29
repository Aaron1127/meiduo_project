from django.shortcuts import render
from django.views import View

from verifications.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http

# Create your views here.


class ImageCodeView(View):

    def get(self, request, uuid):

        # 生成圖形驗證碼
        text, image = captcha.generate_captcha()

        # 保存圖形驗證碼
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, 300, text)

        # 返回圖形驗證碼
        return http.HttpResponse(image, content_type='image/jpg')