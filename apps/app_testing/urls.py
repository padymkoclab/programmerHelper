
from django.conf.urls import url

from .views import TestingSuitDetailView

app_name = 'app_testing'

urlpatterns = [
    url(r'suit/(?P<slug>[-\w]+)/$', TestingSuitDetailView.as_view(), {}, 'suit'),
]
