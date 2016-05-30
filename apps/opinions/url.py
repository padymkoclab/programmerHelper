
from django.conf.urls import url

name = 'opinions'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
