
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


class UserNotificationQuerySet(models.QuerySet):

    def users_with_total_count_notifications(self):

        return self.annotate(total_count_notifications=models.Count('notifications', distinct=True))

    def users_with_count_read_notifications(self):

        return self.annotate(count_read_notifications=models.Sum(
            models.Case(
                models.When(notifications__is_read=True, then=1),
                output_field=models.IntegerField(),
            )
        ))

    def users_with_count_unread_notifications(self):

        return self.annotate(count_unread_notifications=models.Sum(
            models.Case(
                models.When(notifications__is_read=False, then=1),
                output_field=models.IntegerField(),
            )
        ))

    def users_with_count_deleted_notifications(self):

        return self.annotate(count_deleted_notifications=models.Sum(
            models.Case(
                models.When(notifications__is_deleted=True, then=1),
                output_field=models.IntegerField(),
            )
        ))

    def users_with_count_deleted_read_unread_and_total_notifications(self):

        self = self.users_with_total_count_notifications()
        self = self.users_with_count_read_notifications()
        self = self.users_with_count_unread_notifications()
        self = self.users_with_count_deleted_notifications()

        return self
