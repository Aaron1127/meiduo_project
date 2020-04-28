from django.shortcuts import render, reverse, redirect
from django.views import View
from django import http
import re
from django.db import DatabaseError
from users.models import User
from django.contrib.auth import login
from meiduo_mall.utils.response_code import RETCODE

# Create your views here.


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

        if allow != 'on':
            return http.HttpResponseForbidden("請勾選用戶協議");

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)

        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '註冊失敗'})

        # 登入狀態保持
        login(request, user)

        return redirect(reverse('contents:index'))
