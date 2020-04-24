from django.conf.urls import url
# from .views import RegisterView
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]