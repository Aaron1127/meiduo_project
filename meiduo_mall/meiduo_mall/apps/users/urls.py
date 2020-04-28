from django.conf.urls import url
# from .views import RegisterView
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    url(r'^usernames/(?P<username>[0-9a-zA-z_-]{5,20})/count', views.UsernameCountView.as_view()),
]