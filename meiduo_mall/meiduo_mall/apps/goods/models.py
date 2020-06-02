from django.db import models

from meiduo_mall.utils.models import BaseModel
# Create your models here.


class GoodsCategory(BaseModel):
    """商品類別"""
    name = models.CharField(max_length=10, verbose_name='名稱')
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父類別')

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品類別'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsChannelGroup(BaseModel):
    """商品頻道組"""
    name = models.CharField(max_length=20, verbose_name='頻道組名')

    class Meta:
        db_table = 'tb_channel_group'
        verbose_name = '商品頻道組'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsChannel(BaseModel):
    """商品頻道"""
    group = models.ForeignKey(GoodsChannelGroup, verbose_name='頻道組名')
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='頂級商品類別')
    url = models.CharField(max_length=50, verbose_name='頻道頁面鏈接')
    sequence = models.IntegerField(verbose_name='組內順序')

    class Meta:
        db_table = 'tb_goods_channel'
        verbose_name = '商品頻道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class Brand(BaseModel):
    """品牌"""
    name = models.CharField(max_length=20, verbose_name='名稱')
    logo = models.ImageField(verbose_name='Logo圖片')
    first_letter = models.CharField(max_length=1, verbose_name='品牌首字母')

    class Meta:
        db_table = 'tb_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SPU(BaseModel):
    """商品PU"""
    name = models.CharField(max_length=50, verbose_name='名稱')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
    category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat1_spu', verbose_name='一級類別')
    category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat2_spu', verbose_name='二級類別')
    category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat3_spu', verbose_name='三級類別')
    sales = models.IntegerField(default=0, verbose_name='銷量')
    comments = models.IntegerField(default=0, verbose_name='評價數')
    desc_detail = models.TextField(default='', verbose_name='詳細介紹')
    desc_pack = models.TextField(default='', verbose_name='包裝訊息')
    desc_service = models.TextField(default='', verbose_name='售後服務')

    class Meta:
        db_table = 'tb_spu'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SKU(BaseModel):
    """商品SKU"""
    name = models.CharField(max_length=50, verbose_name='名稱')
    caption = models.CharField(max_length=100, verbose_name='副標題')
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, verbose_name='商品')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, verbose_name='從屬類別')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='單價')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='進階')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市場價')
    stock = models.IntegerField(default=0, verbose_name='庫存')
    sales = models.IntegerField(default=0, verbose_name='銷量')
    comments = models.IntegerField(default=0, verbose_name='評價數')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架銷售')
    default_image = models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='默認圖片')

    class Meta:
        db_table = 'tb_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class SKUImage(BaseModel):
    """SKU圖片"""
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku')
    image = models.ImageField(verbose_name='圖片')

    class Meta:
        db_table = 'tb_sku_image'
        verbose_name = 'SKU圖片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.sku.name, self.id)


class SPUSpecification(BaseModel):
    """商品SPU規格"""
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, related_name='specs', verbose_name='商品SPU')
    name = models.CharField(max_length=20, verbose_name='規格名稱')

    class Meta:
        db_table = 'tb_spu_specification'
        verbose_name = '商品SPU規格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.spu.name, self.name)


class SpecificationOption(BaseModel):
    """規格選項"""
    spec = models.ForeignKey(SPUSpecification, related_name='options', on_delete=models.CASCADE, verbose_name='規格')
    value = models.CharField(max_length=20, verbose_name='選項值')

    class Meta:
        db_table = 'tb_specification_option'
        verbose_name = '規格選項'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s - %s' % (self.spec, self.value)


class SKUSpecification(BaseModel):
    """SKU具體規格"""
    sku = models.ForeignKey(SKU, related_name='specs', on_delete=models.CASCADE, verbose_name='sku')
    spec = models.ForeignKey(SPUSpecification, on_delete=models.PROTECT, verbose_name='規格名稱')
    option = models.ForeignKey(SpecificationOption, on_delete=models.PROTECT, verbose_name='規格值')

    class Meta:
        db_table = 'tb_sku_specification'
        verbose_name = 'SKU規格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s - %s' % (self.sku, self.spec.name, self.option.value)
