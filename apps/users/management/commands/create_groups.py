
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from ...constants import GROUPS_NAMES


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    help = 'Create groups for users'

    def handle(self, *args, **kwargs):

        created_groups = list()

        for group_name in GROUPS_NAMES:

            if not Group.objects.filter(name__exact=group_name).exists():
                group = Group.objects.create(name=group_name)
                created_groups.append(group)

        msg_count_objects = 'In the database already {} groups.'.format(Group.objects.count())

        if created_groups:
            msg_new_groups = 'Was created new groups: {}'.format(', '.join(map(str, created_groups)))
        else:
            msg_new_groups = 'New groups was not created'

        logger.info('{} {}'.format(msg_count_objects, msg_new_groups))

        forgotten_names_groups = [
            i for i in Group.objects.values_list('name', flat=True)
            if i not in GROUPS_NAMES
        ]

        if forgotten_names_groups:
            logger.warning('In the database exists groups with outdated name: {}'.format(
                ', '.join(forgotten_names_groups)
            ))
