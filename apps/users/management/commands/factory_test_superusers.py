
from utils.django.basecommands import ExtendedBaseCommand
from utils.python.logging_utils import create_logger_by_filename

from apps.users.factories import UserFactory


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory a given amount users.'

    def add_arguments(self, parser):

        # require single argument from 1 to 999
        parser.add_argument(
            'count_objects',
            nargs=1,
            type=self._positive_integer_from_1_to_999,
        )

    def handle(self, *args, **kwargs):

        # clear all records, about the levels of users, in database
        # User.objects.filter().delete()

        # create levels of users
        count_objects = kwargs['count_objects'][0]
        for i in range(count_objects):
            UserFactory(is_active=True, is_superuser=True)
        logger.debug('Made factory %d superusers.' % count_objects)
