import os

from dcbase.base_settings import *


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'whosgoing',
    'allauth.socialaccount.providers.google',
) + INSTALLED_APPS

ROOT_URLCONF = 'whosgoingsite.urls'
WSGI_APPLICATION = 'whosgoingsite.wsgi.application'

LOGIN_REDIRECT_URL = 'home'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
