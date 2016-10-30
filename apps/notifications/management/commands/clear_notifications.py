
import logging

from django.core.management import BaseCommand

from ...models import Notification


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        Notification._default_manager.filter().delete()

        logger.debug('Cleared all notifications')
