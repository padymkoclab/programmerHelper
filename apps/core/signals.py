
import uuid

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_save, post_save, m2m_changed, pre_delete, post_delete
# from django.core.exceptions import ValidationError
# from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
# from django.conf import settings
# from django.contrib.auth import get_user_model

from apps.notifications.signals import notify

from apps.notifications.models import Notification
from apps.polls.models import Vote
from apps.users.models import User

from apps.notifications.constants import Actions

from .helpers import check_badges_for_instance_and_notify, make_notification


# @receiver(post_save, dispatch_uid=uuid.uuid4)
def post_added_updated_object(sender, instance, created, **kwargs):

    action = 'created' if created is True else 'updated'

    make_notification(sender, instance, action)

    check_badges_for_instance_and_notify(sender, instance)


# @receiver(pre_delete, dispatch_uid=uuid.uuid4)
def pre_deleted_object(sender, instance, **kwargs):
    pass


@receiver(pre_delete, dispatch_uid=uuid.uuid4)
def post_deleted_object(sender, instance, **kwargs):

    # make_notification(sender, instance, 'deleted')
    check_badges_for_instance_and_notify(sender, instance)


# @receiver(user_logged_in, dispatch_uid=uuid.uuid4)
def login_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        user=user,
        action=Actions.USER_LOGGED_IN.value,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
    )


# @receiver(user_logged_out, dispatch_uid=uuid.uuid4)
def logout_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        user=user,
        action=Actions.USER_LOGGED_OUT.value,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
    )


# @receiver(user_login_failed, dispatch_uid=uuid.uuid4)
def failed_login_user(sender, credentials, **kwargs):

    notify.send(
        sender,
        user=None,
        is_anonimuos=True,
        action=Actions.USER_LOGIN_FAILED.value,
        target=None,
        action_target=None,
        level=Notification.ERROR,
    )
