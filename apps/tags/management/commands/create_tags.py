
from django.core.management.base import BaseCommand

from apps.tags.constants import TAGS_NAMES
from apps.tags.factories import TagFactory
from apps.tags.models import Tag

from utils.python.logging_utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


class Command(BaseCommand):

    help = 'Create tags for all project'

    def handle(self, *args, **kwargs):

        # create tags if not yet
        if not Tag.objects.filter().count():
            for tag_name in TAGS_NAMES:
                TagFactory(name=tag_name)
            logger.info('Created tags for a whole project.')
        logger.debug('Tags already presents in database.')
