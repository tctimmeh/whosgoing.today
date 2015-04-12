import os

from dcbase.base_settings import *


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'whosgoing',
    'allauth.socialaccount.providers.google',

    'django_comments',
    'mptt',
    'tagging',
    'zinnia',
    'rest_framework',
    'django_extensions',
) + INSTALLED_APPS

TEMPLATE_CONTEXT_PROCESSORS = (
    'whosgoing.context_processor.whosgoing',
    'zinnia.context_processors.version',
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

ZINNIA_MARKUP_LANGUAGE = 'markdown'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'PAGE_SIZE': 20,
}
