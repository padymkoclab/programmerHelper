
from django.conf.urls import url

from .views import AccountDetailView


app_name = 'app_accounts'

urlpatterns = [
    url(r'detail/(?P<account_email>\w+@[-_\w]+.\w+)/$', AccountDetailView.as_view(), {}, 'detail'),
    url(r'create/$', AccountDetailView.as_view(), {}, 'create'),
    url(r'update/$', AccountDetailView.as_view(), {}, 'update'),
    url(r'delete/$', AccountDetailView.as_view(), {}, 'delete'),
]
