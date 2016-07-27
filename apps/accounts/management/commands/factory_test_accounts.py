
from mylabour.basecommands import ExtendedBaseCommand
from mylabour.utils import create_logger_by_filename

from apps.accounts.factories import AccountFactory
from apps.accounts.models import Account


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory a given amount accounts.'

    def add_arguments(self, parser):

        # require single argument from 1 to 999
        parser.add_argument(
            'count_objects',
            nargs=1,
            type=self._positive_integer_from_1_to_999,
        )

    def handle(self, *args, **kwargs):

        # clear all records, about the levels of accounts, in database
        Account.objects.filter().delete()

        # create levels of accounts
        count_objects = kwargs['count_objects'][0]
        for i in range(count_objects):
            AccountFactory()
        logger.debug('Made factory %d accounts.' % count_objects)
