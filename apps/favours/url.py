
from django.conf.urls import url

name = 'favours'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
