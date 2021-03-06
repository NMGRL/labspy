"""
Django settings for labman project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import pymysql
pymysql.install_as_MySQLdb()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['nmgrl.nmbgmr.nmt.edu', '129.138.12.10']
FORCE_SCRIPT_NAME = '/labs/argon/labspy'
CRISPY_TEMPLATE_PACK = 'bootstrap'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'django_tables2',
    'crispy_forms',
    'leaflet',
    'djangobower',
    'rest_framework',

    # local
    'samples',
    'status',
    'importer'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'labspy.urls'

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'labspy/templates')],
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
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

WSGI_APPLICATION = 'labspy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.environ.get('ARGONSERVER_DB_USER'),
        'PASSWORD': os.environ.get('ARGONSERVER_DB_PWD'),
        'HOST': os.environ.get('ARGONSERVER_HOST'),
        'NAME': 'labspy'
    }
}

# import dj_database_url
# DATABASES['default'] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

TIME_ZONE = 'America/Denver'
# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/labs/argon/labspy/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "labspy/static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'djangobower.finders.BowerFinder',)
# AUTH_USER_MODEL = 'django.contrib.auth.User'

# Leaflet
# http://leafletjs.com/
from leaflet_conf import config

LEAFLET_CONFIG = config()

BOWER_INSTALLED_APPS = (
    'jquery',
    'underscore',
    'flot')

GITHUB_DATA_ORGANIZATION = 'NMGRLData'
GITHUB_DATA_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'PAGE_SIZE': 10
}