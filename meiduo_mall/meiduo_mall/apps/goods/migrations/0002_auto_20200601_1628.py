# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-06-01 08:28
from __future__ import unicode_literals

from django.db import migrations
from django import db


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField('sku', 'default_image_url', db.models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='默認圖片'))
    ]