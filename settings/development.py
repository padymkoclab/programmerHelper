
from .base import *


DEBUG = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_setting_from_file(BASE_DIR.child('secrets.json'), 'DATABASE_NAME'),
        'USER': get_setting_from_file(BASE_DIR.child('secrets.json'), 'DATABASE_USER'),
        'PASSWORD': get_setting_from_file(BASE_DIR.child('secrets.json'), 'DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '',
        'TEST': {
            'NAME': 'test_programmerhelper_db',
            'CHARSET': 'UTF-8',
        },
        'ATOMIC_REQUESTS': True,
    }
}


MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'utils.django.middleware.DebugMiddleware',
]

INTERNAL_IPS = '127.0.0.1'

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]
