
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

        qs = super(NotificationBadgeManager, self).get_queryset()
        qs = qs.filter(action__in=(Actions.LOST_BADGE.value, Actions.EARNED_BADGE.value))
        qs = qs.select_related('recipient', 'actor', 'target_content_type', 'action_target_content_type')
        # qs = qs.prefetch_related('recipient__badges__badge', 'actor__badges__badge')
        return qs


class NotificationActivityManager(models.Manager):
    """

    """

    def get_queryset(self):

        qs = super(NotificationActivityManager, self).get_queryset()
        qs = qs.filter(
            action__in=(
                Actions.ADDED_OBJECT.value,
                Actions.ADDED_USER.value,
                Actions.ADDED_VOTE.value,
                Actions.ADDED_OPINION.value,
                Actions.ADDED_COMMENT.value,
                Actions.ADDED_MARK.value,
                Actions.ADDED_ANSWER.value,
                Actions.ADDED_REPLY.value,
                Actions.ADDED_POST.value,
                Actions.UPDATED_OBJECT.value,
                Actions.UPDATED_USER.value,
                Actions.UPDATED_VOTE.value,
                Actions.UPDATED_OPINION.value,
                Actions.UPDATED_COMMENT.value,
                Actions.UPDATED_MARK.value,
                Actions.UPDATED_ANSWER.value,
                Actions.UPDATED_REPLY.value,
                Actions.UPDATED_POST.value,
                Actions.UPDATED_PROFILE.value,
                Actions.UPDATED_DIARY.value,
                Actions.DELETED_OBJECT.value,
                Actions.DELETED_USER.value,
                Actions.DELETED_OPINION.value,
                Actions.DELETED_COMMENT.value,
                Actions.DELETED_MARK.value,
                Actions.DELETED_REPLY.value,
                Actions.DELETED_POST.value,
                Actions.DELETED_ANSWER.value,
                Actions.DELETED_VOTE.value,
                Actions.USER_LOGGED_IN.value,
                Actions.USER_LOGGED_OUT.value,
                Actions.USER_LOGIN_FAILED.value,
                Actions.USER_ADDED_TO_GROUP.value,
                Actions.USER_REMOVED_FROM_GROUP.value,
            )
        )
        qs = qs.select_related('recipient', 'actor', 'target_content_type', 'action_target_content_type')
        # qs = qs.prefetch_related('recipient__badges__badge', 'actor__badges__badge')
        return qs


class NotificationReputationManager(models.Manager):
    """

    """

    def get_queryset(self):

        qs = super(NotificationReputationManager, self).get_queryset()
        qs = qs.filter(action=Actions.UPDATED_REPUTATION.value)
        qs = qs.select_related('recipient', 'actor', 'target_content_type', 'action_target_content_type')
        # qs = qs.prefetch_related('recipient__badges__badge', 'actor__badges__badge')
        return qs
