
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
]
