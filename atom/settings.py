"""
Django settings for atom project.

Generated by 'django-admin startproject' using Django 2.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import django_heroku
import os
import logging
import environ
from django.utils.translation import ugettext_lazy as _


env = environ.Env()
# herokuの環境かどうか。第一引数に値が入っていなければ、false。
HEROKU_ENV = env.bool('DJANGO_HEROKU_ENV', default=False)

# herokuの環境でない時は.envファイルを読む
if not HEROKU_ENV:
    env.read_env('.env')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'app',
    'api',
    'rest_framework',
    'corsheaders',
    'social_django',
    'snowpenguin.django.recaptcha2',
    'guardian',
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# メールサーバーへの接続設定
# Gmailサーバーを経由
EMAIL_HOST = env("GMAIL_HOST")
EMAIL_HOST_USER = env("GMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("GMAIL_HOST_PASSWORD")
EMAIL_POST = env("GMAIL_POST")
EMAIL_USE_TLS = True


DEFAULT_FROM_EMAIL = env("GMAIL_HOST_USER")

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:index'
LOGOUT_REDIRECT_URL = 'users:login'

# http://yuki-yamashita.site/blog/post/django-recaptchaV2-how-to/
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")

# usersアプリケーション内で設定するUserというモデル(カスタムユーザーモデル)を、
# このプロジェクトのUserモデルとして利用。
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'atom.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

WSGI_APPLICATION = 'atom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': env("DB_HOST"),
            'PORT': env("DB_POST"),
        }
    }


# Heroku
# Activate Django-Heroku.
django_heroku.settings(locals())


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('ja', '日本語'),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# https://www.valentinog.com/blog/drf/#Django_REST_with_React_setting_up_React_and_webpack
# disable the browseable API in production with this configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

# NOTE: 末尾に設置する
# クロスドメイン（異なるドメイン間）でのRequestを許可し、
# 同一ドメインでのRequestのように処理できるようになるライブラリ。
# React（localhost:3000）からDjango（localhost:8000）のAPIを叩く際に必要。
CORS_ORIGIN_WHITELIST = (
    'localhost:3000/',
    'localhost:3000',
)
