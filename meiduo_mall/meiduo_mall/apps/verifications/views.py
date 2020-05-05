from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django import http
import random, logging

from verifications.libs.captcha.captcha import captcha
from . import constants
from meiduo_mall.utils.response_code import RETCODE
# Create your views here.

# 日誌輸出器
logger = logging.getLogger('django')


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

        # 建立redis連接
        redis_conn = get_redis_connection('verify_code')

        # 判斷是否已是否頻繁發送簡訊驗證碼
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '發送簡訊驗證碼過於頻繁'})

        # 提取圖型驗證碼
        image_code_server = redis_conn.get('img_%s' % uuid)

        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '圖形驗證碼已失效'})

        # 對比圖形驗證碼
        image_code_server = image_code_server.decode()  # 將byte轉成字符串
        if image_code_client.lower() != image_code_server.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '輸入的圖形驗證碼有誤'})

        # 刪除圖形驗證碼 避免惡意測試
        redis_conn.delete('img_%s' % uuid)

        # 生成簡訊驗證碼
        # sms_code = '%06d' % random.randint(0, 999999)
        sms_code = '123456'
        logger.info(sms_code)

        # 保存簡訊驗證碼
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存已發送簡訊驗證碼標記
        redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

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
