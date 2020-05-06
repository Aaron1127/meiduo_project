# 定義任務
from celery_tasks.main import celery_app


# 使用裝飾器裝飾異步任務,保證celery識別任務
@celery_app.task(bind=True, name='send_sms_code', retry_backoff=3)
def send_sms_code(self, mobile, sms_code):

    # 發送簡訊驗證碼
    # TO DO
    print(mobile, sms_code)

    return 0

