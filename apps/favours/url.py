
from django.conf.urls import url

app_name = 'favours'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
