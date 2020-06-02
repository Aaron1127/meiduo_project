from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator, EmptyPage

from goods.models import GoodsCategory, SKU
from contents.utils import get_categories
from goods.utils import get_breadcrumb
from meiduo_mall.utils.response_code import RETCODE
# Create your views here.


class DetailView(View):
    """商品詳情頁"""

    def get(self, request, sku_id):
        return render(request, 'detail.html')


class HotGoodsView(View):
    """熱銷排行"""

    def get(self, request, category_id):
        """查詢指定分類的sku訊息,需上架且由銷量高排到低,取前兩名"""

        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 構造JSON數據
        hot_skus = []
        for sku in skus:
            sku_dict = {
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url,
            }
            hot_skus.append(sku_dict)

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_skus': hot_skus})


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
        #skus = SKU.objects.filter(category=category, is_launched=True).order_by(sort_field)
        skus = category.sku_set.filter(is_launched=True).order_by(sort_field)

        # 創建分頁器
        paginator = Paginator(skus, 5)

        try:
            # 獲取用戶當前要看的那頁紀錄
            page_skus = paginator.page(page_num)

        except EmptyPage:
            return http.HttpResponseNotFound('Empty page')

        # 總頁數
        total_pages = paginator.num_pages

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'page_skus': page_skus,
            'total_page': total_pages,
            'page_num': page_num,
            'sort': sort,
            'category_id': category_id,
        }

        return render(request, 'list.html', context)





