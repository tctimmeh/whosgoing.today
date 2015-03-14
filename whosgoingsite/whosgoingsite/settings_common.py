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

TEMPLATE_CONTEXT_PROCESSORS = (
    'whosgoing.context_processor.whosgoing',
) + TEMPLATE_CONTEXT_PROCESSORS

TIME_INPUT_FORMATS = (
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
    '%I:%M %p',     # '02:30 PM'
)

ROOT_URLCONF = 'whosgoingsite.urls'
WSGI_APPLICATION = 'whosgoingsite.wsgi.application'

LOGIN_REDIRECT_URL = 'whosgoing:home'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
