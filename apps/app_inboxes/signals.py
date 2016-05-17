# import uuid

from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.app_inboxes.models import Inbox

from .models import Account


@receiver(post_save)
def autocreate_inbox_and_event_messages_for_new_account(sender, instance, created, *args, **kwargs):
    if created and isinstance(instance, Account):
        message = 'Good time of day dear {0.username}, you succefully created account. Now you can ...'.format(instance)
        Inbox.objects.create(
            account=instance,
            message=message,
        )
