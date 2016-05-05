
from django.conf.urls import url

from .views import TestSuitDetailView

app_name = 'app_programming_tester'

urlpatterns = [
    url(r'test_suit/(?P<slug>[-\w]+)/$', TestSuitDetailView.as_view(), {}, 'test_suit'),
]
