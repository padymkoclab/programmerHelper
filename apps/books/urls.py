
from django.conf.urls import url

from .views import BookDetailView, WriterDetailView, PublisherDetailView

app_name = 'books'

urlpatterns = [
    url(r'book/(?P<slug>[-_\w]+)/$', BookDetailView.as_view(), {}, 'book'),
    url(r'writer/(?P<slug>[-_\w]+)/$', WriterDetailView.as_view(), {}, 'writer'),
    url(r'publisher/(?P<slug>[-_\w]+)/$', PublisherDetailView.as_view(), {}, 'publisher'),
]
