from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """自定義用戶模型類"""
    mobile = models.CharField(max_length=10, unique=True, verbose_name='手機號碼')

    class Meta:
        db_table = 'tb_users'  # 自定義表名
        verbose_name = '用戶'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
