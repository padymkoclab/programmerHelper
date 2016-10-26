
import collections
# import functools

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .utils import BADGES_CHECKERS


class BadgeQuerySet(models.QuerySet):
    """

    """

    def last_got_badges(self, count_last_getting=10):
        """Getting listing last getting badges of accounts."""

        pass


class BadgeManager(models.Manager):
    """
    Model manager for working with badges of account
    """

    def check_badge_for_user(self, badge_name, user):

        from .models import GotBadge, Badge

        badge = Badge.objects.get(name=badge_name)

        checker = BADGES_CHECKERS[badge_name]

        must_has_badge = checker(user)

        if must_has_badge is True and not self.has_badge(badge, user):

            # create a row and send a notification
            GotBadge.objects.create(badge=badge, user=user)
            Notification.objects.send_notification_about_earned_badge(badge, user)

        elif must_has_badge is False and self.has_badge(badge, user):

            # delete a row and send a notification
            GotBadge.objects.get(badge=badge, user=user).delete()
            Notification.objects.send_notification_about_lost_badge(badge, user)

    def check_badge_for_users(self, badge_name):

        from .models import GotBadge, Badge

        badge = Badge.objects.get(name=badge_name)

        checker = BADGES_CHECKERS[badge_name]

        for user in self.prefetch_related('badges'):

            must_has_badge = checker(user)

            if must_has_badge is True and not self.has_badge(badge, user):

                # create a row and send a notification
                GotBadge.objects.create(badge=badge, user=user)
                Notification.objects.send_notification_about_earned_badge(badge, user)

            elif must_has_badge is False and self.has_badge(badge, user):

                # delete a row and send a notification
                GotBadge.objects.get(badge=badge, user=user).delete()
                Notification.objects.send_notification_about_lost_badge(badge, user)

    def has_badge(self, badge, user):
        """ """

        return user.badges.filter(badge=badge).exists()

    def users_with_badge(self, badge_name):
        """Return objects with certain the badge."""

        pass
