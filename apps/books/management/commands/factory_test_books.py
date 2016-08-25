
from mylabour.basecommands import ExtendedBaseCommand
from mylabour.utils import create_logger_by_filename

from apps.books.factories import BookFactory
from apps.books.models import Book, Writer

logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory a passed count of writers for testing.'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):
        count = kwargs.get('count')[0]

        Book.objects.filter().delete()

        if Writer.objects.count() < 4:
            self.call_command('factory_test_writers', '4')

        for i in range(count):
            BookFactory()

        logger.debug('Factoried writers in count: {0}'.format(count))
