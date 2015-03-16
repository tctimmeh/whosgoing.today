from .settings_common import *


SECRET_KEY = '0k&(29rhh!ler7e9wg0c!0_@=25br*+)j2lp15j3n2o_69rduw'

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ZINNIA_PAGINATION = 5
