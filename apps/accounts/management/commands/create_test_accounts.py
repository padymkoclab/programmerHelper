
import argparse

from django.core.management.base import BaseCommand

from mylabour.utils import create_logger_by_filename

from apps.accounts.factories import AccountFactory
from apps.accounts.models import Account


class Command(BaseCommand):

    help = 'Create accounts for tests'
    logger = create_logger_by_filename(__name__)

    def add_arguments(self, parser):

        # require single argument from 1 to 999
        parser.add_argument(
            'count_objects',
            nargs=1,
            type=self._positive_integer_from_1_to_999,
        )

    def _positive_integer_from_1_to_999(self, value):
        """Check up argument."""

        value = int(value)
        if value not in range(1, 1000, 1):
            msg = '%d is an invalid positive integer in range from 1 to 999'
            raise argparse.ArgumentTypeError(msg % value)
        return value

    def handle(self, *args, **options):

        # clear all records, about the levels of accounts, in database
        Account.objects.filter().delete()

        # create levels of accounts
        count_objects = options['count_objects'][0]
        for i in range(count_objects):
            AccountFactory()
        self.logger.debug('Successful created %d account(s) for testing.' % count_objects)
