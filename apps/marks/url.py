
from django.conf.urls import url

name = 'marks'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
