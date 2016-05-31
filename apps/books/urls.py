
from django.conf.urls import url

from .views import BookDetailView, WritterDetailView

app_name = 'books'

urlpatterns = [
    url(r'book/(?P<slug>[-_\w]+)/$', BookDetailView.as_view(), {}, 'book'),
    url(r'writter/(?P<slug>[-_\w]+)/$', WritterDetailView.as_view(), {}, 'writter'),
]
