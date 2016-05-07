
from django.conf.urls import url

from .views import ThemeDetailView, TopicDetailView


app_name = 'app_forum'

urlpatterns = [
    url(r'theme/(?P<slug>[-_\w]+)/$', ThemeDetailView.as_view(), {}, 'theme'),
    url(r'topic/(?P<slug>[-_\w]+)/$', TopicDetailView.as_view(), {}, 'topic'),
]
