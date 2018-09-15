"""
Django settings
"""

import os, sys

######################################
# 兼容 windows 和 linux
######################################
import pymysql

pymysql.install_as_MySQLdb()

###########################
# 项目目录
###########################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 自建APP
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 第三方APP
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

###########################
# 项目安全配置
###########################
SECRET_KEY = '*55o_1#ukq&w2^b%^4i!(i*%5s8x1k59v^t3r^w7@9__n55^5i'

DEBUG = True

ALLOWED_HOSTS = ['*']

###########################
# 项目 APP 注册配置
###########################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'article',
]

###########################
# 项目中间件配置
###########################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

###########################
# 项目路由入口
###########################
ROOT_URLCONF = 'blog.urls'

###########################
# 项目模板目录配置
###########################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Media 配置
                'django.template.context_processors.media',
            ],
        },
    },
]

###########################
# 项目 wsgi
###########################
WSGI_APPLICATION = 'blog.wsgi.application'

###########################
# 项目数据库连接配置
###########################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'blog',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD': '123456',
#     }
# }

###########################
# 项目认证配置
###########################
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

###########################
# 项目其它基础配置
###########################
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

###########################
# 项目静态文件配置
###########################
STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

###########################
# 上传文件配置
###########################
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

###########################
# 分页规则
###########################
PAGINATION_SETTINGS = {
    # 中间部分显示的页码数
    'PAGE_RANGE_DISPLAYED': 5,
    # 前后页码数
    'MARGIN_PAGES_DISPLAYED': 2,
    # 是否显示第一页
    'SHOW_FIRST_PAGE_WHEN_INVALID': False,
}

###########################
# 项目访问地址
###########################
SERVICE_URL = 'http://127.0.0.1'


###########################
# 站长名字
###########################
OWNER_NAME = 'Dy1an'


