
from django.conf.urls import url

from .views import ProgrammingCategoryDetailView


app_name = 'app_programming_utilities'

urlpatterns = [
    url(r'programming_category/(?P<slug>[-_\w]+)/$', ProgrammingCategoryDetailView.as_view(), {}, 'programming_category'),
]
