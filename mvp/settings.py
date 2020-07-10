"""
Django settings for mvp project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8z2y^ew%$yl_pfnq&8s5p9_v!o8s#s9xdn4c#cq8o5m6edh6!8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "ec2-13-209-41-169.ap-northeast-2.compute.amazonaws.com",
    ".hiim.kr"
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'register.apps.RegisterConfig',
    'main.apps.MainConfig',
    'dansang.apps.DansangConfig',
    'everyday.apps.EverydayConfig',
    'history.apps.HistoryConfig',
    'crispy_forms',
    'dynamic_formsets',
    'mathfilters',
    'bootstrap_datepicker_plus',  
    'bootstrap4',
    'django_summernote',
    'emoji_picker',
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

ROOT_URLCONF = 'mvp.urls'

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

WSGI_APPLICATION = 'mvp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

import os
from .local_settings import PG_HOST

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'hiimDB',
        'USER' : 'hiimManager',
        'PASSWORD' : 'hiimxoxo',
        'HOST' : PG_HOST,
        'PORT' : '',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME' : 'hiimmvp',  이거 뭐더라?
        'USER' : 'hiimmvp',
        'PASSWORD' : 'shris9494',
        'HOST' : PG_HOST,
        'PORT' : '',
    }
}
'''
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SUMMERNOTE_CONFIG = {
    'iframe': False,
    'lang' : 'ko-KR',
    'summernote': {
        'width': '100%',
        'height': '450px',
        'placeholder':'위대한 글은 위대한 첫 문장에서 시작됩니다!',
        'toolbar': [
            ['style', ['style',]],
            ['font', ['fontsize', 'bold', 'italic', 'strikethrough']],  # 'fontname', 'clear', ...
            ['color', ['forecolor', ]], # 'backcolor'
            ['para', ['ul', 'ol', 'height']],
            ['insert', ['link']],
            ['misc', ['picture', 'fullscreen', 'print', 'help', ]], # 'codeview', ...
        ],
    },
    'js': (
        '/static/summernote-ext-print.js',
    ),
    'js_for_inplace': (
        '/static/summernote-ext-print.js',
    ),
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/theme/base16-dark.min.css',
        '/mvp/static/summernote.css',
    ),
    'css_for_inplace': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/theme/base16-dark.min.css',
        '/summernote.css',
    ),
    'codemirror': {
        'theme': 'base16-dark',
        'mode': 'htmlmixed',
        'lineNumbers': 'true',
    },
    'lazy': False,
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

BOOTSTRAP4 = {
    'include_jquery': True,
}

SUMMERNOTE_THEME = 'bs4'
X_FRAME_OPTIONS = 'SAMEORIGIN'

STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'main/static'),
    os.path.join(BASE_DIR, 'dansang/static'),
    os.path.join(BASE_DIR, 'register/static'),
    os.path.join(BASE_DIR, 'everyday/static'),
    os.path.join(BASE_DIR, 'history/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'djangobower.finders.BowerFinder'
]

BOWER_COMPONENTS_ROOT = '/PROJECT_ROOT/components/'
BOWER_INSTALLED_APPS = (
    'jquery',
    'jquery-ui',
    'bootstrap'
)

CRISPY_TEMPLATE_PACK="bootstrap4"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login"

# Media 추가할 때 이거 해줘야됨. Telusko 튜토리얼 2시간 18분부터 봐라
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')