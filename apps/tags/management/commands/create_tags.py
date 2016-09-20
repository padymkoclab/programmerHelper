
import logging

from django.core.management.base import BaseCommand

from apps.tags.constants import TAGS_NAMES
from apps.tags.factories import TagFactory
from apps.tags.models import Tag


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    help = 'Create tags for a whole project'

    def handle(self, *args, **kwargs):

        if not Tag.objects.exists():

            for tag_name in TAGS_NAMES:
                TagFactory(name=tag_name)

            logger.info('Created tags for a whole project.')

        logger.debug('Tags already presents in database.')
