
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from apps.users.constants import SUPERUSER_DATA


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    help = 'Creating a superuser for debug.'

    def handle(self, *args, **kwargs):

        # get a user model for project
        User = get_user_model()

        # create a superuser if yet does not exists
        # or return message that it already exists
        try:
            user = User.objects.get_by_natural_key(SUPERUSER_DATA[User.USERNAME_FIELD])
        except User.DoesNotExist:
            user = User.objects.create_superuser(**SUPERUSER_DATA)
            logger.info('Added superuser "{}"'.format(user))
        else:
            logger.warning('Superuser "{}" already exist.'.format(user))

        group = Group.objects.get(name='moderators')
        user.groups.add(group)
