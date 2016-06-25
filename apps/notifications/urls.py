
from django.conf.urls import url

from .views import NotificationDetailView


name = 'notifications'

urlpatterns = [
    url(r'notification/(?P<account_email>[-\w]+@[-\w]+.\w+)/$', NotificationDetailView.as_view(), {}, 'notification'),
]
