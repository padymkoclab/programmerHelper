
from django.conf.urls import url

app_name = 'app_favours'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
