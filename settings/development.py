
from .base import *


DEBUG = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret_value_for_setting_from_file(filename='secrets.json', setting_name='DATABASE_NAME'),
        'USER': get_secret_value_for_setting_from_file(filename='secrets.json', setting_name='DATABASE_USER'),
        'PASSWORD': get_secret_value_for_setting_from_file(filename='secrets.json', setting_name='DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '',
        'TEST': {
            'NAME': 'test_programmerhelper_db',
            'CHARSET': 'UTF-8',
        },
        'ATOMIC_REQUESTS': True,
    }
}


INSTALLED_APPS += ['django_extensions', 'debug_toolbar']
