"""
Django Blog Settings
"""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%=wx)hfh(xgo_)d^2%#+s!vjre(o8h7*d*s(oz)ij8dveeen5u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PROJECT_NAME = "django-blog"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "simpleui",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 自动补全
    "dal",
    "dal_select2",
    # 富文本编辑
    "ckeditor",
    # 上传图片
    "ckeditor_uploader",
    "rest_framework",
    "drf_yasg",

    "django_blog",
    "apps.blog",
    "apps.config",
    "apps.comment",

]
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 2,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_blog.urls'
# 主题
THEME = "default"
# 首页title
HOME_TITLE = "django-blog".title()
# 页面底部 POWER_BY xxx
POWER_BY = "mikgio"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "themes", THEME, "template")],
        # 自动查找app中的templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "themes", THEME, "static"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
CKEDITOR_UPLOAD_PATH = "article_images"
WSGI_APPLICATION = 'django_blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


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

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# ====== SIMPLEUI =========

SIMPLEUI_LOGO = ""

# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_ANALYSIS = False

SIMPLEUI_CONFIG = {
    "menu_display": [
        "博客",
        "评论",
        "配置",
        "认证和授权",
    ]
}
# 最近动作
SIMPLEUI_HOME_ACTION = False
# 快速操作
SIMPLEUI_HOME_QUICK = True
# 服务器信息
SIMPLEUI_HOME_INFO = False
# 默认主题
# SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 400,
        "width": "full",
        "tabSpaces": 4,
        # 代码插件
        "extraPlugins": "codesnippet",
    },
}
