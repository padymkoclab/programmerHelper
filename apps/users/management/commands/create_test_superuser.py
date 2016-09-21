
import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.users.constants import TEST_SUPERUSER_DATA


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    help = 'Creating a superuser fo testing or debug.'

    def handle(self, *args, **kwargs):

        # get a user model for project
        User = get_user_model()

        # create a superuser if yet does not exists
        # or return message that it already exists
        try:
            User.objects.get_by_natural_key(TEST_SUPERUSER_DATA[User.USERNAME_FIELD])
        except User.DoesNotExist:
            get_user_model().objects.create_superuser(**TEST_SUPERUSER_DATA)
            logger.info('Succesful added superuser with {0} "{1}"!'.format(
                User.USERNAME_FIELD,
                TEST_SUPERUSER_DATA[User.USERNAME_FIELD],
            ))
        else:
            logger.warning(
                'Superuser with %s "%s" already exist.' % (
                    User.USERNAME_FIELD, TEST_SUPERUSER_DATA[User.USERNAME_FIELD]
                )
            )
