
from django.conf.urls import url

from .views import ArticleDetailView

app_name = 'articles'

urlpatterns = [
    url(
        r'articles/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<slug>[-\w]+)/$',
        ArticleDetailView.as_view(), {}, 'article'
    ),
]
