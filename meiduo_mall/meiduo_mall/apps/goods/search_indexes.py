from haystack import indexes

from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引數據模型類"""

    # 接收索引欄位, 使用文檔定義索引欄位, 並且使用模板語法渲染
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回建立索引的模型類"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的數據查詢集"""
        return self.get_model().objects.filter(is_launched=True)

