
from django.conf.urls import url

app_name = 'app_comments'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
