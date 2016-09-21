
import logging

from django.core.management.base import BaseCommand

from apps.users.factories import LevelFactory
from apps.users.constants import USER_LEVEL_DATAS


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    help = 'Create all levels of users'

    def handle(self, *args, **options):

        LevelModel = LevelFactory._meta.model

        if not LevelModel.objects.count():
            for obj in USER_LEVEL_DATAS:
                LevelFactory(name=obj.name, color=obj.color, description=obj.description)
            logger.info('Created levels for users.')
        logger.debug('Levels of users already exists.')
