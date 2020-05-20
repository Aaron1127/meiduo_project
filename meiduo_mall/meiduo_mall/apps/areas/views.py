from django.shortcuts import render
from django.views import View
from django import http
import logging
from django.core.cache import cache

from areas.models import Area
from meiduo_mall.utils.response_code import RETCODE
# Create your views here.

logger = logging.getLogger('django')


class AreasView(View):
    """省市區三級連動"""

    def get(self, request):

        area_id = request.GET.get('area_id')
        if not area_id:

            # 判斷是否有緩存
            province_list = cache.get('province_list')
            if not province_list:
                try:
                    # 查詢省級數據
                    province_model_list = Area.objects.filter(parent__isnull=True)

                    # 需要將模型列表轉成字典列表
                    province_list = []
                    for province_model in province_model_list:
                        province = {
                            'id': province_model.id,
                            'name': province_model.name
                        }
                        province_list.append(province)

                    # 緩存省分字典列表數據,默認存儲到別名為default的配置中
                    cache.set('province_list', province_list, 3600)

                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '查詢省分數據錯誤'})

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})

        else:
            # 判斷是否有緩存
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                try:
                    # 查詢市區級數據
                    parent_model = Area.objects.get(id=area_id)
                    sub_model_list = parent_model.subs.all()

                    # 將子級模型列表轉成字典列表
                    subs = []
                    for sub_model in sub_model_list:
                        sub_dict = {
                            'id': sub_model.id,
                            'name': sub_model.name
                        }
                        subs.append(sub_dict)

                    # 構造子級JSON
                    sub_data = {
                        'id': parent_model.id,
                        'name': parent_model.name,
                        'subs': subs
                    }

                    # 緩存城市或區縣
                    cache.set('sub_area_' + area_id, sub_data, 3600)

                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '查詢城市或區縣數據錯誤'})

            # 響應城市或區縣的JSON數據
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data})













