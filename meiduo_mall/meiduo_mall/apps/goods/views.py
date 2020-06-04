from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone

from goods.models import GoodsCategory, SKU, GoodsVisitCount
from contents.utils import get_categories
from goods.utils import get_breadcrumb
from meiduo_mall.utils.response_code import RETCODE
# Create your views here.


class DetailVisitView(View):
    """統計分類商品的訪問量"""

    def post(self, request, category_id):

        # 接收校驗參數
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('category_id不存在')

        # 獲取當天日期
        t = timezone.localtime()

        # 統計指定分類商品的訪問量
        counts_data = GoodsVisitCount.objects.filter(date=, category=category)




class DetailView(View):
    """商品詳情頁"""

    def get(self, request, sku_id):
        """提供商品詳情頁"""

        # 接收參數和校驗參數
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return render(request, '404.html')

        # 查詢商品分類
        categories = get_categories()

        # 查詢麵包屑導航
        breadcrump = get_breadcrumb(sku.category)

        # 構建當前商品的規格
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 獲取當前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 構建不同規格參數(選項)的sku字典
        spec_sku_map = {}
        for s in skus:
            # 獲取sku的規格參數
            s_specs = s.specs.order_by('spec_id')
            # 用於形成規格參數-sku字典的鍵
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向規格參數-sku字典添加紀錄
            spec_sku_map[tuple(key)] = s.id
        # 獲取當前商品的規格訊息
        goods_specs = sku.spu.specs.order_by('id')
        # 若當前sku的規格訊息不完整，則不再繼續
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 複製當前sku的規格鍵
            key = sku_key[:]
            # 該規格的選項
            spec_options = spec.options.all()
            for option in spec_options:
                # 在規格參數sku字典中查找符合當前規格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        # 構造上下文
        context = {
            'categories': categories,
            'breadcrumb': breadcrump,
            'sku': sku,
            'specs': goods_specs,
        }

        return render(request, 'detail.html', context)


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





