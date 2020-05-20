from django.db import models

# Create your models here.


class Area(models.Model):
    """省市區"""
    name = models.CharField(max_length=20, verbose_name='名稱')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上級行政區劃')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市區'
        verbose_name_plural = '省市區'

    def __str__(self):
        return self.name
