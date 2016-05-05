
from django.conf.urls import url

from .views import TagDetailView

app_name = 'app_tags'

urlpatterns = [
    url(r'tag/(?P<slug>[-_\w]+)/$', TagDetailView.as_view(), {}, 'tag'),
]
