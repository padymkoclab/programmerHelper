
from django.utils.text import force_text
from django.dispatch import receiver
# from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.core.signals import request_finished
from django.contrib.auth import get_user_model

from apps.users.models import Profile
from apps.diaries.models import Diary
from apps.polls.models import Poll, Vote

from .models import Notification


User = get_user_model()


@receiver(post_save, sender=User)
def created_updated_user(sender, instance, created, *args, **kwargs):

    if created is True:
        Notification.objects.send_notification_about_created_new_user(instance)
    else:
        Notification.objects.send_notification_about_updated_data_of_user(instance)


@receiver(post_save, sender=Profile)
def updated_profile(sender, instance, created, *args, **kwargs):

    if created is False:
        Notification.objects.send_notification_about_updated_profile_of_user(instance.user)


@receiver(post_save, sender=Diary)
def updated_diary(sender, instance, created, *args, **kwargs):

    if created is False:
        Notification.objects.send_notification_about_updated_diary_of_user(instance.user)


@receiver(post_save)
def particitated_in_poll(sender, instance, created, *args, **kwargs):

    if created is True:

        if sender == Vote:

            poll, user = instance.poll, instance.user

            Notification.objects.send_notification_about_created_object(
                user,
                _('You participated in the poll "{}"').format(poll),
            )

            User.badges_manager.check_badge_for_user('Voter', user)
            User.badges_manager.check_badge_for_user('Electorate', user)
            User.badges_manager.check_badge_for_user('Vox Populi', user)

        elif sender == Poll:

            User.badges_manager.check_badge_for_users('Electorate')
            User.badges_manager.check_badge_for_users('Vox Populi')


@receiver(post_delete)
def lost_vote_in_poll(sender, instance, *args, **kwargs):

    if sender == Vote:

        poll, user = instance.poll, instance.user

        Notification.objects.send_notification_about_created_object(
            user,
            _('You lost vote in the poll "{}"').format(poll),
        )

        User.badges_manager.check_badge_for_user('Voter', user)
        User.badges_manager.check_badge_for_user('Electorate', user)
        User.badges_manager.check_badge_for_user('Vox Populi', user)

    elif sender == Poll:

        User.badges_manager.check_badge_for_users('Electorate')
        User.badges_manager.check_badge_for_users('Vox Populi')
