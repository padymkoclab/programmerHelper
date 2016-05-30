
from django.conf.urls import url

name = 'subscribers'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
