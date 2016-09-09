
from django.conf.urls import url

from .views import SolutionDetailView


app_name = 'solutions'

urlpatterns = [
    url(r'solution/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<slug>[-_\w]+)/$', SolutionDetailView.as_view(), {}, 'solution'),
]
