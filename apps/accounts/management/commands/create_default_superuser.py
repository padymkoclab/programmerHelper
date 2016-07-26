
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from mylabour.utils import create_logger_by_filename

from apps.accounts.constants import DEFAULT_SUPERUSER_DATA


logger = create_logger_by_filename(__name__)


class Command(BaseCommand):

    help = 'Creating a default superuser'

    def handle(self, *args, **kwargs):

        # get a user model for project
        Account = get_user_model()

        # create a superuser if yet does not exists
        # or return message that it already exists
        try:
            Account.objects.get_by_natural_key(DEFAULT_SUPERUSER_DATA['email'])
        except Account.DoesNotExist:
            get_user_model().objects.create_superuser(**DEFAULT_SUPERUSER_DATA)
            logger.info('Succesful added superuser!')
        else:
            logger.warning(
                'Superuser with %s "%s" already exist.' % (
                    Account.USERNAME_FIELD, DEFAULT_SUPERUSER_DATA['email']
                )
            )
