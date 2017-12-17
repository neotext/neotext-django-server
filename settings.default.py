"""
Django settings for neotext project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_READ_URL = 'http://read.neotext.net'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '12345#!67890abcdefghizxy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# NEOTEXT SETTINGS
JSON_FILE_PATH = "/Library/WebServer/Documents/quote/sha1/"
VERSION_NUM = '0.02'
NUM_DOWNLOAD_PROCESSES = 25  # num citations downloaded simultaneously
DOWNLOAD_TIMEOUT = 5         # num seconds to wait on download

""" algorithm used to generate hash key: ('sha1','md5','sha256')
    note: changing algorithm requires adding support to backend
    if using a relational db, may require new/different column definition
"""
HASH_ALGORITHM = 'sha1'


# AMAZON S3 Login information
AMAZON_ACCESS_KEY = '123243545789459063022'
AMAZON_SECRET_KEY = 'alksjdfla;jkdfklajkfgjaklrekgljreklgsdfl'
AMAZON_S3_BUCKET = 'read.neotext.net'
AMAZON_S3_ENDPOINT = 's3.amazonaws.com'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
        'GET',  # Get rid of 'GET' eventually
        'POST',
)


CORS_ALLOW_HEADERS = (
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admindocs',
    # 'django_extensions',
    'neotext',
    'corsheaders',
)

CORS_EXPOSE_HEADERS = ()
CORS_PREFLIGHT_MAX_AGE = 86400
CORS_ALLOW_CREDENTIALS = False
CORS_REPLACE_HTTPS_REFERER = False


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'neotext.urls'

WSGI_APPLICATION = 'neotext.wsgi.application'

# Database: for syntax for Postgres settings, see URL below:
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'optional_postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'neotext',
        'USER': 'neotext_webserver',
        'PASSWORD': 'kalsjt35wlk54jlks',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 30,
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
            'CULL_FREQUENCY': 2,
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    '/home/timlangeman/webapps/static_neotext/',
    '/Users/timlangeman/Sites/neotext/neotext/templates/',
    '/Users/timlangeman/Sites/neotext/neotext/static/',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMIN_MEDIA_PREFIX = '/static/admin/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
