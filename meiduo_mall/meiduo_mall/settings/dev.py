"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(sys.path)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# print(sys.path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x)0zvvas01#@rlyy0%_==kid7#f=mas-wj!ccgj3)m+zasb$jl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.meiduo.site', '127.0.0.1']


# Application definition

# 要做模板或遷移的子應用才需要註冊

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'haystack',  # 全文檢索

    'users',  # 用戶模塊
    'contents',  # 首頁廣告模塊
    'areas',  # 省市區三及連動
    'goods',  # 商品模塊
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        # 'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        # 'APP_DIRS': True,
        # 'OPTIONS': {
        #     'context_processors': [
        #         'django.template.context_processors.debug',
        #         'django.template.context_processors.request',
        #         'django.contrib.auth.context_processors.auth',
        #         'django.contrib.messages.context_processors.messages',
        #     ],
        # },
        'BACKEND': 'django.template.backends.jinja2.Jinja2', # 配置jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 補充jinja2模板引擎環境
            'environment': 'meiduo_mall.utils.jinja2_env.jinja2_environment',
        },

    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.181.135',
        'PORT': 3306,
        'USER': 'aaron',
        'PASSWORD': 'p1p9p8p1',
        'NAME': 'meiduo',
    }
}

# 配置redis數據庫
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.181.135/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.181.135/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.181.135/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 用戶商品瀏覽紀錄
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://192.168.181.135/3",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 指定加載靜態文件的路由前綴
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已經存在的日誌器
    'formatters': {  # 日誌信息顯示格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 對日誌進行過濾
        'require_debug_true': {  # django在debug模式下才輸出日誌
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日誌處理方法
        'console': {  # 向終端輸出日誌
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件輸出日誌
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日誌文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日誌器
        'django': {  # 定義了一個名為django的日誌器
            'handlers': ['console', 'file'],  # 可以同時向終端與文件輸出日誌
            'propagate': True,  # 是否繼續傳遞日誌訊息
            'level': 'INFO',  # 日誌器接收的最低日誌級別
        },
    }
}

AUTH_USER_MODEL = 'users.User'

# 指定自定義用戶認證後端
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileBackend']

# 判斷用戶是否登入後, 指定未登入用戶重定向的地址
LOGIN_URL = '/login/'

# 郵件參數
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'aaronltc1127@gmail.com'
EMAIL_HOST_PASSWORD = 'rnzhfzeugcudvpbb'
EMAIL_FROM = '美多商城<aaronltc1127@gmail.com>'

# 郵箱認證地址
EMAIL_VERIFY_URL = 'http://www.meiduo.site:8000/emails/verification/'

# 指定自定義的Django文件儲存類
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.fdfs_storage.FastDFSStorage'

# FastDFS相關參數
# FDFS_BASE_URL = 'http://192.168.181.135:8888/'
FDFS_BASE_URL = 'http://image.meiduo.site:8888/'

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.181.135:9200/', # Elasticsearch伺服器IP位置，port固定為9200
        'INDEX_NAME': 'meiduo_mall', # Elasticsearch建立的索引庫名稱
    },
}

# 當添加、修改、刪除數據時，自動生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 每頁顯示幾條搜索數據
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5

