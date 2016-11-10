
import uuid
import collections

from django.contrib.auth.models import Group
# from django.core.exceptions import ValidationError
from django.dispatch import Signal, receiver

from .models import Notification
from .constants import Actions


notify = Signal(providing_args=[
    'actor', 'target', 'action', 'is_public', 'is_emailed', 'level', 'action_target', 'recipient'
])


@receiver(notify, dispatch_uid=uuid.uuid4)
def handle_notify(sender, **kwargs):

    actor = kwargs.get('actor')
    target = kwargs.get('target')
    action = kwargs.get('action')
    is_public = kwargs.get('is_public')
    is_emailed = kwargs.get('is_emailed')
    is_deleted = kwargs.get('is_deleted')
    level = kwargs.get('level')
    action_target = kwargs.get('action_target')
    recipient = kwargs.get('recipient')

    options = dict(
        actor=actor,
        target=target,
        action=action,
        level=level,
        action_target=action_target,
    )

    if is_public is not None:
        options['is_public'] = is_public

    if is_emailed is not None:
        options['is_emailed'] = is_emailed

    if is_deleted is not None:
        options['is_deleted'] = is_deleted

    if isinstance(recipient, collections.Iterable):
        recipients = set()
        for obj in recipient:
            if isinstance(obj, Group):
                recipients.update(frozenset(obj.user_set.all()))
            else:
                recipients.add(obj)
    else:
        if isinstance(recipient, Group):
            recipients = recipient.user_set.iterator()
        else:
            recipients = frozenset({recipient})

    for recipient in recipients:

        options['recipient'] = recipient

        notification = Notification(**options)
        if action == Actions.DELETED_USER.value:
            notification.actor = None
        notification.full_clean()
        # reqired additional variables
        notification.save(actor=actor, target=target)
