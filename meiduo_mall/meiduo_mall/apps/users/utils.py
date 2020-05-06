# 自定義用戶認證後端,實現多帳戶登入

from django.contrib.auth.backends import ModelBackend
import re

from users.models import User


def get_user_by_account(account):
    """
    通過帳號獲取用戶
    :param account: 用戶名或手機號碼
    :return: user
    """
    try:
        if re.match(r'^09\d{8}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileBackend(ModelBackend):
    """自定義用戶認證後端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重寫用戶認證方法
        :param request:
        :param username: 用戶名或手機號碼
        :param password: 密碼
        :param kwargs:
        :return:
        """
        # 查詢用戶
        user = get_user_by_account(username)

        if user and user.check_password(password):
            return user
        else:
            return None


