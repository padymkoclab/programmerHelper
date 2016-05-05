
from django.conf.urls import url

from .views import ThemeDetailView, TopicDetailView


app_name = 'app_forum'

urlpatterns = [
    url(r'topic_category/(?P<slug>[-_\w]+)/$', ThemeDetailView.as_view(), {}, 'topic_category'),
    url(r'topic/(?P<slug>[-_\w]+)/$', TopicDetailView.as_view(), {}, 'topic'),
]
