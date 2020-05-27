from django.shortcuts import render
from django.views import View
from collections import OrderedDict

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
# Create your views here.


class IndexView(View):
    """首頁廣告"""

    def get(self, request):
        """提供首頁廣告頁面"""

        # 準備商品分類對應的字典(有序字典)
        categories = OrderedDict()

        # 查詢所有的商品頻道,要排序
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')

        for channel in channels:
            # 獲取當前頻道所在組
            group_id = channel.group_id

            if group_id not in categories:
                categories[group_id] = {'channels': [], 'sub_cats': []}

            # 查詢當前頻道對應的一級類別
            cat1 = channel.category

            categories[group_id]['channels'].append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            })

            # 查尋二級和三級類別
            for cat2 in cat1.subs.all():
                cat2.sub_cats = []
                for cat3 in cat2.subs.all():
                    cat2.sub_cats.append(cat3)

            categories[group_id]['sub_cats'].append(cat2)

            # 構造上下文
            context = {
                'categories': categories,
            }

        return render(request, 'index.html', context)


