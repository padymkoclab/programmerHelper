
from utils.python.logging_utils import create_logger_by_filename
from utils.django.basecommands import ExtendedBaseCommand

from ...factories import SnippetFactory


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory test snippets'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        SnippetModel = SnippetFactory._meta.model
        SnippetModel._default_manager.filter().delete()

        for i in range(count):
            SnippetFactory()

        logger.debug('Made factory {} snippets'.format(
            SnippetModel._default_manager.count()
        ))
