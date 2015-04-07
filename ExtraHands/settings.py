"""
Django settings for ExtraHands project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.contrib.messages import constants as messages
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cw%s9g0seh*e0t=3(7r)dp9ea^)1tr8y4l763d_55-93x0=6^0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'extra_hands_app',
    'rolepermissions',
    'datetimewidget',
    'debug_toolbar',
    'mail_templated',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ExtraHands.urls'

WSGI_APPLICATION = 'ExtraHands.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS=(os.path.join(BASE_DIR, 'assets'),)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)


ROLEPERMISSIONS_MODULE = 'ExtraHands.roles'

LOGON_REDIRECT_URL = '/myaccount/'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # django.contrib.staticfiles.finders.DefaultStorageFinder',
)

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'eugene.baibourin@gmail.com'
EMAIL_HOST_PASSWORD = '3lxuGYo51ENYy3UuYVfQzA'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# This works!
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'laura.baibourine@gmail.com'
# EMAIL_HOST_PASSWORD = 'sezozwdivdqfojzl'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True