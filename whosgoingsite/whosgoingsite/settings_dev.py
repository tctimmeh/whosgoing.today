import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from dcbase.base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0k&(29rhh!ler7e9wg0c!0_@=25br*+)j2lp15j3n2o_69rduw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'whosgoing',
    'allauth.socialaccount.providers.google',
) + INSTALLED_APPS

ROOT_URLCONF = 'whosgoingsite.urls'
WSGI_APPLICATION = 'whosgoingsite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ACCOUNT_EMAIL_VERIFICATION = 'optional'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
