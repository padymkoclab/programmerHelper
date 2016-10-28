
import collections

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from apps.polls.models import Poll, Vote, Choice

from .constants import Badges
from .querysets import BadgeQuerySet


class BadgeManager(models.Manager):
    """
    Model manager for working with badges
    """

    def check_badges_for_instance(self, instance):

        users_lost_badges, users_earned_badges = collections.defaultdict(set), collections.defaultdict(set)

        users = self.get_users(instance)

        if users.exists():

            if isinstance(instance, (Poll, Choice, Vote)):

                badge_const = Badges.Badge.VOTER_BRONZE
                checker_args = (Vote, )

                users_lost_badges, users_earned_badges = self.update_badges_and_return_result(
                    users, badge_const, users_lost_badges, users_earned_badges, checker_args
                )

                badge_const = Badges.Badge.VOTER_SILVER
                checker_args = (Vote, Poll)

                users_lost_badges, users_earned_badges = self.update_badges_and_return_result(
                    users, badge_const, users_lost_badges, users_earned_badges, checker_args
                )

                badge_const = Badges.Badge.VOTER_GOLD
                checker_args = (Vote, Poll)

                users_lost_badges, users_earned_badges = self.update_badges_and_return_result(
                    users, badge_const, users_lost_badges, users_earned_badges, checker_args
                )

        return users_lost_badges, users_earned_badges

    def check_badge(self, badge_const, users, *args):

        checker = Badges.checkers[badge_const]
        users_lost_badge, users_earned_badge = checker(users, *args)
        return users_lost_badge, users_earned_badge

    def has_badge(self, badge, user):
        """ """

        from .models import EarnedBadge

        return EarnedBadge._default_manager.filter(badge=badge, user=user).exists()

    def users_with_badge(self, badge_const):
        """Return objects with certain the badge."""

        pass

    def show_tree_badges(self, user=None):
        """Display badges earned and unearned, next as tree view."""

        return NotImplementedError

    def get_users(self, instance):

        User = get_user_model()

        if isinstance(instance, Poll):
            users = User._default_manager.filter(pk__in=instance.votes.values('user'))

        elif isinstance(instance, Vote):
            users = User._default_manager.filter(pk=instance.user.pk)
            assert users.count() == 1

        elif isinstance(instance, Choice):
            users = User._default_manager.filter(pk=instance.votes.values('user'))

        elif isinstance(instance, User):
            users = User._default_manager.filter(pk=instance.pk)

        return users

    def update_badges_and_return_result(self, users, badge_const, users_lost_badges, users_earned_badges, checker_args):

        from .models import EarnedBadge

        badge = self.get(name=badge_const.value)

        users_lost_badge, users_earned_badge = self.check_badge(badge_const, users, *checker_args)

        for user in users_lost_badge:

            if self.has_badge(badge, user):

                EarnedBadge.objects.delete_if_exists(user, badge)

                users_lost_badges[user].add(badge)

        for user in users_earned_badge:

            if not self.has_badge(badge, user):

                earned_badge = EarnedBadge(user=user, badge=badge)
                earned_badge.full_clean()
                earned_badge.save()

                users_earned_badges[user].add(badge)

        return users_lost_badges, users_earned_badges


BadgeManager = BadgeManager.from_queryset(BadgeQuerySet)


class EarnedBadgeManager(models.Manager):
    """

    """

    def delete_if_exists(self, user, badge):

        try:
            earned_badge = self.get(user=user, badge=badge)
        except self.model.DoesNotExist:
            pass
        else:
            earned_badge.delete()
