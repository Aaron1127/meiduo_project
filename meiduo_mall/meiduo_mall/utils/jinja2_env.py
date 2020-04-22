from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage


def jinja2_environment(**option):
    """jinja2環境"""

    # 創建環境對象
    env = Environment(**option)

    # 自定義語法 {{ static('靜態文件相對路徑') }} {{ url('路由的命名空間') }}
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })

    # 返回環境對象
    return env
