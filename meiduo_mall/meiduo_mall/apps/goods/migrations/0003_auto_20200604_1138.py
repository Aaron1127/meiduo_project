# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-06-04 03:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20200601_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsVisitCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('count', models.IntegerField(default=0, verbose_name='訪問量')),
                ('date', models.DateField(auto_now_add=True, verbose_name='統計日期')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品分類')),
            ],
            options={
                'verbose_name': '統計分類商品訪問量',
                'verbose_name_plural': '統計分類商品訪問量',
                'db_table': 'tb_goods_visit',
            },
        ),
    ]
