
from django.conf.urls import url

from .views import SnippetDetailView


app_name = 'app_snippets'

urlpatterns = [
    url(r'snippet/(?P<slug>[-_\w]+)/$', SnippetDetailView.as_view(), {}, 'snippet'),
]
