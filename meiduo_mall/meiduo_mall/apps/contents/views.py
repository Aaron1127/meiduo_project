from django.shortcuts import render
from django.views import View

# Create your views here.


class IndexView(View):
    """首頁廣告"""

    def get(self, request):

        return render(request, 'index.html')


