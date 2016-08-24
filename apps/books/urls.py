
from django.conf.urls import url

from .views import BookDetailView, WriterDetailView

app_name = 'books'

urlpatterns = [
    url(r'book/(?P<slug>[-_\w]+)/$', BookDetailView.as_view(), {}, 'book'),
    url(r'writer/(?P<slug>[-_\w]+)/$', WriterDetailView.as_view(), {}, 'writer'),
]
