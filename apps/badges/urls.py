
from django.conf.urls import url

from .views import BadgeDetailView


app_name = 'badges'


urlpatterns = (
    url(
        r'badge/(?P<pk>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<slug>[-\w]+)/$',
        BadgeDetailView.as_view(), {}, 'detail'
    ),
)
