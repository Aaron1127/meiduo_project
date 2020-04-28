from django.conf.urls import url
# from .views import RegisterView
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    # 檢查用戶名是否重複
    url(r'^usernames/(?P<username>[0-9a-zA-z_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 檢查用戶手機是否重複
    url(r'^mobiles/(?P<mobile>09\d{8})/count/$', views.MobileCountView.as_view()),
]