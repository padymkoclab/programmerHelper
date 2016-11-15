
import uuid

from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save, pre_delete, m2m_changed
# from django.core.exceptions import ValidationError
# from django.contrib.contenttypes.models import ContentType
# from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
# from django.conf import settings
# from django.contrib.auth import get_user_model

from apps.notifications.signals import notify
from apps.notifications.models import Notification
from apps.notifications.constants import Actions

from .helpers import notify_badges, notify_activity, notify_reputation


@receiver(post_save, dispatch_uid=uuid.uuid4)
def post_added_updated_object(sender, instance, created, **kwargs):

    action = 'created' if created is True else 'updated'

    notify_activity(sender, instance, action)
    notify_badges(sender, instance)
    notify_reputation(sender, instance, action, users_for_deleting=None)


@receiver(pre_delete, dispatch_uid=uuid.uuid4)
def pre_deleted_object(sender, instance, **kwargs):

    action = 'deleted'

    users_for_deleting = kwargs.get('users_for_deleting')

    notify_activity(sender, instance, action, users_for_deleting=users_for_deleting)
    notify_badges(sender, instance, users_for_deleting=users_for_deleting)
    notify_reputation(sender, instance, action, users_for_deleting=users_for_deleting)


@receiver(user_logged_in, dispatch_uid=uuid.uuid4)
def login_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        actor=user,
        action=Actions.USER_LOGGED_IN.value,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
        recipient=Group.objects.get(name='moderators'),
    )


@receiver(user_logged_out, dispatch_uid=uuid.uuid4)
def logout_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        actor=user,
        action=Actions.USER_LOGGED_OUT.value,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
        recipient=Group.objects.get(name='moderators'),
    )


@receiver(user_login_failed, dispatch_uid=uuid.uuid4)
def failed_login_user(sender, credentials, **kwargs):

    notify.send(
        sender,
        actor=None,
        is_anonimuos=True,
        action=Actions.USER_LOGIN_FAILED.value,
        target=None,
        action_target=None,
        level=Notification.ERROR,
        recipient=Group.objects.get(name='moderators'),
    )


@receiver(m2m_changed, sender=Group.user_set.through, dispatch_uid=uuid.uuid4)
def changed_group(sender, instance, action, reverse, model, pk_set, **kwargs):

    if action not in ('pre_add', 'pre_remove', 'pre_clear'):
        return

    notify_options = dict(
        sender=Group,
        is_anonimuos=False,
        action_target=None,
        level=Notification.SUCCESS,
        recipient=Group.objects.get(name='moderators'),
    )

    if action == 'pre_add':

        notify_options_for_add = dict()
        notify_options_for_add.update(notify_options)
        notify_options_for_add['action'] = Actions.USER_ADDED_TO_GROUP.value

        if reverse is True:
            for user_pk in pk_set:
                if not instance.user_set.filter(pk=user_pk).exists():
                    user = model._default_manager.get(pk=user_pk)
                    notify_options_for_add['recipient'] = user
                    notify_options_for_add['actor'] = user
                    notify_options_for_add['target'] = instance
                    notify.send(**notify_options_for_add)
        else:
            for group_pk in pk_set:
                if not instance.groups.filter(pk=group_pk).exists():
                    group = Group.objects.get(pk=group_pk)
                    notify_options_for_add['recipient'] = instance
                    notify_options_for_add['actor'] = instance
                    notify_options_for_add['target'] = group
                    notify.send(**notify_options_for_add)

    elif action == 'pre_remove':

        notify_options_for_remove = dict()
        notify_options_for_remove.update(notify_options)
        notify_options_for_remove['action'] = Actions.USER_REMOVED_FROM_GROUP.value

        if reverse is True:
            for user_pk in pk_set:
                if instance.user_set.filter(pk=user_pk).exists():
                    user = model._default_manager.get(pk=user_pk)
                    notify_options_for_remove['recipient'] = user
                    notify_options_for_remove['actor'] = user
                    notify_options_for_remove['target'] = instance
                    notify.send(**notify_options_for_remove)
        else:
            for group_pk in pk_set:
                if instance.groups.filter(pk=group_pk).exists():
                    group = Group.objects.get(pk=group_pk)
                    notify_options_for_remove['recipient'] = instance
                    notify_options_for_remove['actor'] = instance
                    notify_options_for_remove['target'] = group
                    notify.send(**notify_options_for_remove)

    elif action == 'pre_clear':

        notify_options_for_clear = dict()
        notify_options_for_clear.update(notify_options)
        notify_options_for_clear['action'] = Actions.USER_REMOVED_FROM_GROUP.value
        if reverse is True:
            for user in instance.user_set.iterator():
                notify_options_for_clear['recipient'] = user
                notify_options_for_clear['actor'] = user
                notify_options_for_clear['target'] = instance
                notify.send(**notify_options_for_clear)
        else:
            for group in instance.groups.iterator():
                notify_options_for_clear['recipient'] = instance
                notify_options_for_clear['actor'] = instance
                notify_options_for_clear['target'] = group
                notify.send(**notify_options_for_clear)
