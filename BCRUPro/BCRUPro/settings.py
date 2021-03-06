"""
Django settings for BCRUPro project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import logging
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y+1v#cnm!+0su^wt&0-fgxk(z_74*_yd=+9mb(z=q-+p^)r=5l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'BCRUPro',
    'login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BCRUPro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {  # Adding this section should work around the issue.
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'BCRUPro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

# Language english
# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

# Language chinaese
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# Using local time when saving data to DB, or will have 8 hours equation of time
USE_TZ = False

SESSION_COOKIE_AGE = 60*60*24


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    # os.path.join(STATIC_ROOT, 'AdminLTE_3_0_5'),
    ("adminlte", os.path.join(STATIC_ROOT, 'AdminLTE_3_0_5')),
    ("img", os.path.join(STATIC_ROOT, 'datatables', 'images')),
    ("js", os.path.join(STATIC_ROOT, 'js')),
    ("fonts", os.path.join(STATIC_ROOT, 'datatables', 'fonts')),
]

sysstr = platform.system()
home_path = ""
if sysstr == 'Linux':
    home_path = os.environ['HOME']
elif sysstr == 'Windows':
    home_path = os.environ['TEMP']
else:
    print("sysstr:", sysstr)
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
console_path = os.path.join(home_path, 'ConsoleLog')
if not os.path.exists(console_path):
    os.makedirs(console_path)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'exhaustive': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(pathname)s:%(lineno)s][%(user)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'consolelogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(console_path, 'console.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 2,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'BCRUPro': {
            'handlers': ['console', 'consolelogfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'login': {
            'handlers': ['console', 'consolelogfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
