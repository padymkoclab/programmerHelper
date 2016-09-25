
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
]
