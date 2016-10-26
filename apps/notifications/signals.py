
import uuid

from django.dispatch import Signal, receiver

from .models import Notification


notify = Signal(providing_args=[
    'actor', 'target', 'action', 'is_public', 'is_emailed'
])


@receiver(notify, dispatch_uid=uuid.uuid4)
def handle_notify(sender, **kwargs):

    actor = kwargs.get('actor')
    target = kwargs.get('target')
    action = kwargs.get('action')
    is_public = kwargs.get('is_public')
    is_emailed = kwargs.get('is_emailed')
    is_deleted = kwargs.get('is_deleted')
    # recipient = kwargs.get('recipient')

    options = dict(
        actor=actor,
        target=target,
        action=action,
    )

    if is_public is not None:
        options['is_public'] = is_public

    if is_emailed is not None:
        options['is_emailed'] = is_emailed

    if is_deleted is not None:
        options['is_deleted'] = is_deleted

    notification = Notification(**options)
    notification.full_clean()
    notification.save()
