
from django.db import models
# from django.utils.translation import ugettext_lazy as _

from .querysets import NotificationQuerySet
from .constants import Actions


class NotificationManager(models.Manager):
    """ """

    def mark_all_as_read(self, recipient=None):
        pass

    def mark_all_as_deleted(self, recipient=None):
        pass

    def mark_all_as_unread(self, recipient=None):
        pass

    def mark_as_deleted(self, recipient=None):
        pass

    def mark_as_unread(self, recipient=None):
        pass

    def mark_as_read(self, recipient=None):
        pass


NotificationManager = NotificationManager.from_queryset(NotificationQuerySet)


class NotificationBadgeManager(models.Manager):
    """

    """

    def get_queryset(self):

        return super(NotificationBadgeManager, self).get_queryset().filter(
            models.Q(action=Actions.DELETED_BADGE.value) | models.Q(action=Actions.ADDED_BADGE.value)
        )
