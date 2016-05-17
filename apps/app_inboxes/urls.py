
from django.conf.urls import url

from .views import InboxDetailView


app_name = 'app_inboxes'

urlpatterns = [
    url(r'inbox/(?P<account_email>[-\w]+@[-\w]+.\w+)/$', InboxDetailView.as_view(), {}, 'inbox'),
]
