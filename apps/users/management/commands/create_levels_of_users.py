
import logging

from django.core.management.base import BaseCommand

from ...constants import LEVELS
from ...factories import LevelFactory


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    help = 'Create all levels of users'

    def handle(self, *args, **options):

        LevelModel = LevelFactory._meta.model

        for attrs in LEVELS:
            LevelModel._default_manager.update_or_create(
                name=attrs['name'],
                defaults={
                    'color': attrs['color'],
                    'description': attrs['description'],
                }
            )
        logger.info('Created/updated levels for users.')
