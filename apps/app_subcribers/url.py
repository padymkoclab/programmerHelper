
from django.conf.urls import url

app_name = 'app_subcribers'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
