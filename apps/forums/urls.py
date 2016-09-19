
from django.conf.urls import url

from .views import ForumDetailView, TopicDetailView


app_name = 'forums'

urlpatterns = [
    url(r'forum/(?P<slug>[-_\w]+)/$', ForumDetailView.as_view(), {}, 'forum'),
    url(r'topic/(?P<slug>[-_\w]+)/$', TopicDetailView.as_view(), {}, 'topic'),
]
