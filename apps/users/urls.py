
from django.conf.urls import url

from .views import UserDetailView


app_name = 'users'

urlpatterns = [
    url(r'detail/(?P<account_email>\w+@[-_\w]+.\w+)/$', UserDetailView.as_view(), {}, 'detail'),
    url(r'create/$', UserDetailView.as_view(), {}, 'create'),
    url(r'update/$', UserDetailView.as_view(), {}, 'update'),
    url(r'delete/$', UserDetailView.as_view(), {}, 'delete'),
    url(r'level/(?P<slug>[-_\w]+)/$', UserDetailView.as_view(), {}, 'level'),
]
