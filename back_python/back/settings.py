"""
Django settings for back project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!*nmutor&f16elc9cb*&8v)e#d9il@u_k$h_u^18#7ozw$uf=z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','mily365.com','www.mily365.com','192.168.2.107','192.168.1.157','192.168.43.207']

WX={
  'WX_APP_ID':'wx8f428820d2150a9e',
  'WX_APP_SECURITY':'751afbe404efaee85ba8638ceeb1dc44',
  'WX_APP_REDIRECT':'http://mily365.com/main?role={role}',
  'WX_AUTH_URL_CODE':"https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&{redirect_uri}&response_type=code&scope=snsapi_userinfo&#wechat_redirect" % ('wx8f428820d2150a9e'),
  'WX_AUTH_URL_INFO':"https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % ('wx8f428820d2150a9e','751afbe404efaee85ba8638ceeb1dc44',"{code}"),
  'WX_AUTH_USER_INFO':"https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"
}

# Application definition
SITE_ID=2
INSTALLED_APPS = [
    'api',
    'cms',
    'front',
    'account',
    'feedback',
    'org',
    'activity',
    'media',
    'habitinfo',
    'sysinfo',
    'school',
    'django_wysiwyg',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# When using TCP connections
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 1,
            'PASSWORD': '123qwe',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        },
    },
}
CACHE_FORMAT_STR={
    # 系统账户ID
    'sys_mily_account_id':1,
    'sys_monkey_account_id':2,
    'account_mily_profileid_key':'account:rice:%d',
    'account_monkey_profileid_key':'account:cash:%d',
    # 缓存习惯类别和习惯难度对应的习惯
   'cat_habit_level':'cat:%d:habit:%s',
   'cat_habit_level_timeout':3600*24*7,
   # 活动历史缓存
   'acthistory_key':'acthistory:%d',
   'acthistory_key_timeout':3600*24*7,
   # 习惯缓存
   'habit_key':'habit:%d',
   'habit_key_timeout':3600*24*10000,
   # 今日打卡缓存
   'actid_userid_habitid_date_key':'feedback:%d:%d:%d:%s',
   'userid_habitid_date_key_timeout':3600*24*2,
   # 最近一次打卡缓存
   'actid_userid_habitid_key':'feedback:%d:%d:%d',
   'userid_habitid_key_timeout':3600*24*365,
   # 体力值缓存,永久
   'body_userid_key':'body:%d',
}
MIDDLEWARE = [
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware', # This must be last
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

ROOT_URLCONF = 'back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'back.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schoolerp',
        'USER':'root',
        'PASSWORD':'viathink@520612',
        'HOST':'mily365.com',
        'PORT':'8306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static/')
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'back/media/')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'log/debug.log'),
        },
        'fileError': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'log/error.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file','fileError'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
