
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class NotificationsConfig(AppConfig):

    name = "apps.notifications"
    verbose_name = _("Notifications")
    label = 'notifications'

    def ready(self):

        from .signals import notify
