
from django.utils.text import force_text
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.core.signals import request_finished

from apps.users.models import Profile, User
from apps.diaries.models import Diary
from apps.polls.models import Vote
from apps.badges.models import Badge, GotBadge

from .models import Notification


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def created_updated_user(sender, instance, created, *args, **kwargs):

    if created is True:
        Notification.objects.create(
            user=instance,
            action=Notification.CREATED_USER,
            content=_('Welcome new user. Your succefully registered. Now you has access to diary and profile too.')
        )
    else:
        Notification.objects.create(
            user=instance,
            action=Notification.UPDATED_USER,
            content=_('Your succefully updated data of your user.'),
        )


@receiver(post_save, sender=Profile)
def updated_profile(sender, instance, created, *args, **kwargs):

    if created is False:
        Notification.objects.create(
            user=instance.user,
            action=Notification.UPDATED_PROFILE,
            content=_('Your succefully updated your profile.'),
        )


@receiver(post_save, sender=Diary)
def updated_diary(sender, instance, created, *args, **kwargs):

    if created is False:
        Notification.objects.create(
            user=instance.user,
            action=Notification.UPDATED_DIARY,
            content=_('Your succefully updated your diarly.'),
        )


badge = Badge.objects.get(name='Voter')


def has_badge(user, badge):

    return user.badges.filter(pk=badge.pk).exists()


def checkup_badge_voter(user):
    return False


@receiver(post_save, sender=Vote)
def particitated_in_poll(sender, instance, created, *args, **kwargs):

    if created is True:

        poll = instance.poll
        user = instance.user
        Notification.objects.create(
            user=user,
            action=Notification.CREATED_OBJECT,
            content=_('You participated in the poll "{}"').format(poll),
        )

        if not has_badge(user, badge):
            GotBadge.objects.create(user=user, badge=badge)


@receiver(post_delete, sender=Vote)
def lost_vote_in_poll(sender, instance, *args, **kwargs):

    poll = instance.poll
    user = instance.user
    if user.get_count_votes() == 0:
        GotBadge.objects.get(user=user, badge=badge).delete()

    Notification.objects.create(
        user=instance.user,
        action=Notification.CREATED_OBJECT,
        content=_('You lost vote in the poll "{}"').format(poll),
    )
