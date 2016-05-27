
from django.conf.urls import url

app_name = 'app_opinions'

urlpatterns = [
    url(r'/$', '.as_view()', {}, ''),
]
