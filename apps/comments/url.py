
from django.conf.urls import url

name = 'comments'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
