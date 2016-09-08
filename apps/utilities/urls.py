
from django.conf.urls import url

from .views import CategoryDetailView


app_name = 'utilities'

urlpatterns = [
    url(r'category/(?P<slug>[-_\w]+)/$', CategoryDetailView.as_view(), {}, 'category'),
]
