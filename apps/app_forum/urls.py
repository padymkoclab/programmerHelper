
from django.conf.urls import url

from .views import SectionDetailView, TopicDetailView


app_name = 'app_forum'

urlpatterns = [
    url(r'theme/(?P<slug>[-_\w]+)/$', SectionDetailView.as_view(), {}, 'theme'),
    url(r'topic/(?P<slug>[-_\w]+)/$', TopicDetailView.as_view(), {}, 'topic'),
]
