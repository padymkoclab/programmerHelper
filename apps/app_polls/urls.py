
from django.conf.urls import url

from .views import PollDetailView

app_name = 'app_polls'

urlpatterns = [
    url(r'poll/(?P<slug>[_\w]+)/$', PollDetailView.as_view(), {}, 'poll'),
]
