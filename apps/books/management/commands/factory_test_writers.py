
from utils.django.basecommands import ExtendedBaseCommand
from utils.python.logging_utils import create_logger_by_filename

from apps.books.factories import WriterFactory
from apps.books.models import Writer

logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory a passed count of writers for testing.'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):
        count = kwargs.get('count')[0]

        Writer.objects.filter().delete()

        for i in range(count):
            WriterFactory()

        logger.debug('Factoried writers in count: {0}'.format(count))
