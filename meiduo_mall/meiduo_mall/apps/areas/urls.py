from django.conf.urls import url

from . import views


urlpatterns = [
    # 省市區三及連動
    url(r'^areas/$', views.AreasView.as_view()),

]
