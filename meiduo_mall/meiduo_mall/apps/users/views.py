from django.shortcuts import render
from django.views import View

# Create your views here.


class RegisterView(View):
    """用戶註冊"""

    def get(self, request):

        return render(request, 'register.html')

