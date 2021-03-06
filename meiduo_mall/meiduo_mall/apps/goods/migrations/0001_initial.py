# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-05-24 02:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('name', models.CharField(max_length=20, verbose_name='名稱')),
                ('logo', models.ImageField(upload_to='', verbose_name='Logo圖片')),
                ('first_letter', models.CharField(max_length=1, verbose_name='品牌首字母')),
            ],
            options={
                'verbose_name': '品牌',
                'verbose_name_plural': '品牌',
                'db_table': 'tb_brand',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('name', models.CharField(max_length=10, verbose_name='名稱')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='goods.GoodsCategory', verbose_name='父類別')),
            ],
            options={
                'verbose_name': '商品類別',
                'verbose_name_plural': '商品類別',
                'db_table': 'tb_goods_category',
            },
        ),
        migrations.CreateModel(
            name='GoodsChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('url', models.CharField(max_length=50, verbose_name='頻道頁面鏈接')),
                ('sequence', models.IntegerField(verbose_name='組內順序')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='頂級商品類別')),
            ],
            options={
                'verbose_name': '商品頻道',
                'verbose_name_plural': '商品頻道',
                'db_table': 'tb_goods_channel',
            },
        ),
        migrations.CreateModel(
            name='GoodsChannelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('name', models.CharField(max_length=20, verbose_name='頻道組名')),
            ],
            options={
                'verbose_name': '商品頻道組',
                'verbose_name_plural': '商品頻道組',
                'db_table': 'tb_channel_group',
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('name', models.CharField(max_length=50, verbose_name='名稱')),
                ('caption', models.CharField(max_length=100, verbose_name='副標題')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='單價')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='進階')),
                ('market_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='市場價')),
                ('stock', models.IntegerField(default=0, verbose_name='庫存')),
                ('sales', models.IntegerField(default=0, verbose_name='銷量')),
                ('comments', models.IntegerField(default=0, verbose_name='評價數')),
                ('is_launched', models.BooleanField(default=True, verbose_name='是否上架銷售')),
                ('default_image', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='默認圖片')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.GoodsCategory', verbose_name='從屬類別')),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
                'db_table': 'tb_sku',
            },
        ),
        migrations.CreateModel(
            name='SKUImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('image', models.ImageField(upload_to='', verbose_name='圖片')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.SKU', verbose_name='sku')),
            ],
            options={
                'verbose_name': 'SKU圖片',
                'verbose_name_plural': 'SKU圖片',
                'db_table': 'tb_sku_image',
            },
        ),
        migrations.CreateModel(
            name='SKUSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
            ],
            options={
                'verbose_name': 'SKU規格',
                'verbose_name_plural': 'SKU規格',
                'db_table': 'tb_sku_specification',
            },
        ),
        migrations.CreateModel(
            name='SpecificationOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('value', models.CharField(max_length=20, verbose_name='選項值')),
            ],
            options={
                'verbose_name': '規格選項',
                'verbose_name_plural': '規格選項',
                'db_table': 'tb_specification_option',
            },
        ),
        migrations.CreateModel(
            name='SPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('name', models.CharField(max_length=50, verbose_name='名稱')),
                ('sales', models.IntegerField(default=0, verbose_name='銷量')),
                ('comments', models.IntegerField(default=0, verbose_name='評價數')),
                ('desc_detail', models.TextField(default='', verbose_name='詳細介紹')),
                ('desc_pack', models.TextField(default='', verbose_name='包裝訊息')),
                ('desc_service', models.TextField(default='', verbose_name='售後服務')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.Brand', verbose_name='品牌')),
                ('category1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat1_spu', to='goods.GoodsCategory', verbose_name='一級類別')),
                ('category2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat2_spu', to='goods.GoodsCategory', verbose_name='二級類別')),
                ('category3', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat3_spu', to='goods.GoodsCategory', verbose_name='三級類別')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
                'db_table': 'tb_spu',
            },
        ),
        migrations.CreateModel(
            name='SPUSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('name', models.CharField(max_length=20, verbose_name='規格名稱')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='goods.SPU', verbose_name='商品SPU')),
            ],
            options={
                'verbose_name': '商品SPU規格',
                'verbose_name_plural': '商品SPU規格',
                'db_table': 'tb_spu_specification',
            },
        ),
        migrations.AddField(
            model_name='specificationoption',
            name='spec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='goods.SPUSpecification', verbose_name='規格'),
        ),
        migrations.AddField(
            model_name='skuspecification',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.SpecificationOption', verbose_name='規格值'),
        ),
        migrations.AddField(
            model_name='skuspecification',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='goods.SKU', verbose_name='sku'),
        ),
        migrations.AddField(
            model_name='skuspecification',
            name='spec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.SPUSpecification', verbose_name='規格名稱'),
        ),
        migrations.AddField(
            model_name='sku',
            name='spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.SPU', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='goodschannel',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsChannelGroup', verbose_name='頻道組名'),
        ),
    ]
