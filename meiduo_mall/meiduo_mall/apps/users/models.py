from django.db import models
from django.contrib.auth.models import AbstractUser

from meiduo_mall.utils.models import BaseModel
# Create your models here.


class User(AbstractUser):
    """自定義用戶模型類"""
    mobile = models.CharField(max_length=10, unique=True, verbose_name='手機號碼')
    email_active = models.BooleanField(default=False, verbose_name='郵箱驗證狀態')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默認地址')

    class Meta:
        db_table = 'tb_users'  # 自定義表名
        verbose_name = '用戶'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用戶')
    title = models.CharField(max_length=20, verbose_name='地址名稱')
    receiver = models.CharField(max_length=20, verbose_name='收貨人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='區')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手機')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定電話')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='電子郵箱')
    is_deleted = models.BooleanField(default=False, verbose_name='邏輯刪除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
