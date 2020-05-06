# Celery的入口文件
from celery import Celery


# 創建Celery實例
celery_app = Celery('meiduo')

# 載入配置文件
celery_app.config_from_object('celery_tasks.config')

# 註冊任務
celery_app.autodiscover_tasks(['celery_tasks.sms'])
