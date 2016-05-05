
from django.conf.urls import url

from .views import AccountDetailView


app_name = 'app_accounts'

urlpatterns = [
    url(r'account_detail/(?P<account_email>\w+@[-_\w]+.\w+)/$', AccountDetailView.as_view(), {}, 'account_detail'),
]
