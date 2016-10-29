
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from .querysets import BadgeQuerySet


class BadgeManager(models.Manager):
    """
    Model manager for working with badges
    """

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


BadgeManager = BadgeManager.from_queryset(BadgeQuerySet)
