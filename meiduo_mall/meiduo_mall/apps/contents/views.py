from django.shortcuts import render
from django.views import View
from collections import OrderedDict

from contents.models import ContentCategory
from contents.utils import get_categories
# Create your views here.


class IndexView(View):
    """首頁廣告"""

    def get(self, request):
        """提供首頁廣告頁面"""

        # 獲取所有商品分類
        categories = get_categories()

        # 查詢首頁廣告數據
        # 查詢所有的廣告類別
        contents = OrderedDict()
        content_categories = ContentCategory.objects.all()
        for content_category in content_categories:
            # 查詢出未下架的廣告並排序
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by('sequence')

        # 構造上下文
        context = {
            'categories': categories,
            'contents': contents,
        }

        return render(request, 'index.html', context)


