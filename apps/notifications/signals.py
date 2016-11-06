
import uuid

from django.core.exceptions import ValidationError
from django.dispatch import Signal, receiver

from .models import Notification


notify = Signal(providing_args=[
    'user', 'target', 'action', 'is_public', 'is_emailed', 'level', 'action_target', 'is_anonimuos'
])


@receiver(notify, dispatch_uid=uuid.uuid4)
def handle_notify(sender, **kwargs):

    user = kwargs.get('user')
    target = kwargs.get('target')
    action = kwargs.get('action')
    is_public = kwargs.get('is_public')
    is_emailed = kwargs.get('is_emailed')
    is_deleted = kwargs.get('is_deleted')
    level = kwargs.get('level')
    action_target = kwargs.get('action_target')
    is_anonimuos = kwargs.get('is_anonimuos')
    # recipient = kwargs.get('recipient')

    options = dict(
        user=user,
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

    if is_anonimuos is not None:
        options['is_anonimuos'] = is_anonimuos

    notification = Notification(**options)

    try:
        notification.full_clean()
    except ValidationError:
        notification.user = None
        notification.full_clean()
    finally:
        notification.save(user=user, target=target)
