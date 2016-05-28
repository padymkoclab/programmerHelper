
from django.conf.urls import url

app_name = 'app_subscribers'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
