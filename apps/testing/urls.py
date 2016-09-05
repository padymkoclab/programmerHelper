
from django.conf.urls import url

from .views import SuitDetailView

app_name = 'testing'

urlpatterns = [
    url(r'suit/(?P<slug>[-\w]+)/$', SuitDetailView.as_view(), {}, 'suit'),
]
