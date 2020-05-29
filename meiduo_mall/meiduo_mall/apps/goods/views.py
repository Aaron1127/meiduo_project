from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator

from goods.models import GoodsCategory
from contents.utils import get_categories
from goods.utils import get_breadcrumb
# Create your views here.


class ListView(View):
    """商品列表頁"""

    def get(self, request, category_id, page_num):
        """查詢並渲染商品表"""

        try:
            category = GoodsCategory.objects.get(id=category_id)

        except GoodsCategory.DoesNotExist:
            http.HttpResponseForbidden('參數category_id不存在')

        # 獲取sort排序, 如果sort沒有值, 默認取default
        sort = request.GET.get('sort', 'default')
        # 根據sort選擇排序欄位,欄位必須是模型類的屬性
        if sort == 'price':
            sort_field = 'price'  # 價格低到高

        elif sort == 'hot':
            sort_field = '-sales'  # 銷量高到低

        else:
            sort = 'default'
            sort_field = 'create_time'

        # 查詢商品分類
        categories = get_categories()

        # 麵包屑導航
        breadcrumb = get_breadcrumb(category)

        # 分頁和排序查詢 category查詢sku 一對多
        skus = category.sku_set.filter(is_launched=True).order_by(sort_field)

        # 創建分頁器
        paginator = Paginator(skus, 5)
        # 總頁數
        total_pages = paginator.num_pages
        # 獲取用戶當前要看的那頁紀錄
        page_skus = paginator.page(page_num)

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
        }

        return render(request, 'list.html', context)





