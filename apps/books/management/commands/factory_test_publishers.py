
from mylabour.basecommands import ExtendedBaseCommand
from mylabour.logging_utils import create_logger_by_filename

from apps.books.factories import PublisherFactory


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory test publishers'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        model = PublisherFactory._meta.model

        model._default_manager.filter().delete()

        for i in range(count):
            PublisherFactory()

        logger.debug('Succefully generated {0} publishers.'.format(model._default_manager.count()))
