
from django.conf.urls import url

from .views import InboxDetailView


name = 'inboxes'

urlpatterns = [
    url(r'inbox/(?P<account_email>[-\w]+@[-\w]+.\w+)/$', InboxDetailView.as_view(), {}, 'inbox'),
]
