
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class NotificationsConfig(AppConfig):

    name = "apps.notifications"
    verbose_name = _("Notifications")
    label = 'notifications'

    def ready(self):

        from .signals import (
            created_updated_user,
            updated_profile,
            updated_diary,
            lost_vote_in_poll,
        )
