
from django.conf.urls import url

from .views import PollDetailView

app_name = 'polls'

urlpatterns = [
    url(r'poll/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<slug>[-\w]+)/$', PollDetailView.as_view(), {}, 'poll'),
]
