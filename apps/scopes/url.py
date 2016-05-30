
from django.conf.urls import url

name = 'scopes'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
