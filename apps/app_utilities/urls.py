
from django.conf.urls import url

from .views import UtilityCategoryDetailView


app_name = 'app_utilities'

urlpatterns = [
    url(r'category/(?P<slug>[-_\w]+)/$', UtilityCategoryDetailView.as_view(), {}, 'category'),
]
