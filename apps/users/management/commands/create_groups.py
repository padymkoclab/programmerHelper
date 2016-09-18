
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from ...constants import GROUPS_NAMES


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    help = 'Create groups for users'

    def handle(self, *args, **kwargs):

        for group_name in GROUPS_NAMES:
            if not Group.objects.filter(name__exact=group_name).exists():
                Group.objects.create(name=group_name)
                logger.debug('Created group "{}"'.format(group_name))
            else:
                logger.debug('Group "{}" already exists.'.format(group_name))
