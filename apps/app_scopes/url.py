
from django.conf.urls import url

app_name = 'app_scopes'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
