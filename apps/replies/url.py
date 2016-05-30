
from django.conf.urls import url

name = 'replies'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
