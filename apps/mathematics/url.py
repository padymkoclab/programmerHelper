
from django.conf.urls import url

app_name = 'app_mathematics'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
