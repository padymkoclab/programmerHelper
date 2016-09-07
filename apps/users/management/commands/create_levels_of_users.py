
from django.core.management.base import BaseCommand

from utils.python.logging_utils import create_logger_by_filename

from apps.users.factories import UserLevelFactory
from apps.users.models import UserLevel
from apps.users.constants import USER_LEVEL_DATAS


logger = create_logger_by_filename(__name__)


class Command(BaseCommand):

    help = 'Create all levels of users'

    def handle(self, *args, **options):

        # create levels of users if don`t yet
        if not UserLevel.objects.count():
            for obj in USER_LEVEL_DATAS:
                UserLevelFactory(name=obj.name, color=obj.color, description=obj.description)
            logger.info('Created levels for users.')
        logger.debug('Levels of users already exists.')
