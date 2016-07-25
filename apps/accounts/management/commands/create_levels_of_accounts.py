
from django.core.management.base import BaseCommand

from mylabour.utils import create_logger_by_filename

from apps.accounts.factories import AccountLevelFactory
from apps.accounts.models import AccountLevel
from apps.accounts.constants import ACCOUNT_LEVEL_DATAS


logger = create_logger_by_filename(__name__)


class Command(BaseCommand):

    help = 'Create all levels of accounts'

    def handle(self, *args, **options):

        # clear all records, about the levels of accounts, in database
        AccountLevel.objects.filter().delete()

        # create levels of accounts
        for obj in ACCOUNT_LEVEL_DATAS:
            AccountLevelFactory(name=obj.name, color=obj.color, description=obj.description)
        logger.info('Successful executed creating levels for accounts')
