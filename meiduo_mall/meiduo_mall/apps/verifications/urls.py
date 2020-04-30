from django.conf.urls import url
from . import views


urlpatterns = [
    # 圖形驗證碼
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    # 簡訊驗證碼
    url(r'^sms_codes/(?P<mobile>09\d{8})/$', views.SMSCodeView.as_view()),
]