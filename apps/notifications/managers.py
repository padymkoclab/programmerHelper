
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .querysets import NotificationQuerySet


class NotificationManager(models.Manager):
    """ """

    def _create_notification(self, user, action, content):
        """ """

        notification = self.model(user=user, action=action, content=content)
        notification.full_clean()
        notification.save()

    def send_notification_about_created_new_user(self, user):
        """ """

        self._create_notification(
            user,
            self.model.CREATED_USER,
            self.model.CONTENTS[self.model.CREATED_USER],
        )

    def send_notification_about_updated_data_of_user(self, user):
        """ """

        self._create_notification(
            user,
            self.model.UPDATED_USER,
            self.model.CONTENTS[self.model.UPDATED_USER],
        )

    def send_notification_about_updated_profile_of_user(self, user):
        """ """

        self._create_notification(
            user,
            self.model.UPDATED_PROFILE,
            self.model.CONTENTS[self.model.UPDATED_PROFILE],
        )

    def send_notification_about_updated_diary_of_user(self, user):

        self._create_notification(
            user,
            self.model.UPDATED_DIARY,
            self.model.CONTENTS[self.model.UPDATED_DIARY],
        )

    def send_notification_about_created_object(self, user, content):
        """ """

        self._create_notification(
            user,
            self.model.CREATED_OBJECT,
            content,
        )

    def send_notification_about_deleted_object(self, user, content):
        """ """

        self._create_notification(
            user,
            self.model.CREATED_OBJECT,
            content,
        )

    def send_notification_about_lost_badge(self, badge, user):
        """ """

        self._create_notification(
            user,
            self.model.LOST_BADGE,
            self.model.CONTENTS[self.model.LOST_BADGE].format(badge),
        )

    def send_notification_about_earned_badge(self, badge, user):
        """ """

        self._create_notification(
            user,
            self.model.EARNED_BADGE,
            self.model.CONTENTS[self.model.EARNED_BADGE].format(badge),
        )


    def mark_all_as_read(self, user=None):
        pass

    def mark_all_as_unread(self, user=None):
        pass


NotificationManager = NotificationManager.from_queryset(NotificationQuerySet)
