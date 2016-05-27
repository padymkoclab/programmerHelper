
from django.conf.urls import url

app_name = 'app_replies'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
