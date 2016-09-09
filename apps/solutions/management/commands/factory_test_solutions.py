
from utils.django.basecommands import ExtendedBaseCommand
from utils.python.logging_utils import create_logger_by_filename

from ...factories import SolutionFactory

logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, **kwargs):

        count = kwargs['count'][0]

        SolutionModel = SolutionFactory._meta.model

        SolutionModel.objects.filter().delete()

        for i in range(count):
            SolutionFactory()

        logger.debug('Made factory {0} solutions'.format(count))
