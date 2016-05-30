
from django.conf.urls import url

from .views import UtilityCategoryDetailView


app_name = 'utilities'

urlpatterns = [
    url(r'category/(?P<slug>[-_\w]+)/$', UtilityCategoryDetailView.as_view(), {}, 'category'),
]
