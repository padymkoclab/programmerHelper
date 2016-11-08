
from django.db import models


class NotificationQuerySet(models.QuerySet):
    """ """

    def only_deleted(self, recipient=None):
        """ """

        return self

    def only_unread(self, include_deleted=False):
        """ """

        return self

    def only_read(self, include_deleted=False):
        """ """

        return self

    def only_non_deleted(self):
        """ """

        return self
