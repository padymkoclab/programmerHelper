
from django.conf.urls import url

from .views import CategoryDetailView, SolutionDetailView


app_name = 'solutions'

urlpatterns = [
    url(r'solution/(?P<slug>[-_\w]+)/$', SolutionDetailView.as_view(), {}, 'solution'),
    url(r'category/(?P<slug>[-_\w]+)/$', CategoryDetailView.as_view(), {}, 'category'),
]
