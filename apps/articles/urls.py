
from django.conf.urls import url

from .views import ArticleDetailView

app_name = 'articles'

urlpatterns = [
    url(r'articles/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), {}, 'article'),
]
