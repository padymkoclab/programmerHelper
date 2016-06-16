
from django.conf.urls import url

from .views import CategoryDetailView, SolutionDetailView


app_name = 'solutions'

urlpatterns = [
    url(r'solution/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<slug>[-_\w]+)/$', SolutionDetailView.as_view(), {}, 'solution'),
    url(r'category/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<slug>[-_\w]+)/$', CategoryDetailView.as_view(), {}, 'category'),
]
