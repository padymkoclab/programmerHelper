
from mylabour.logging_utils import create_logger_by_filename
from mylabour.basecommands import ExtendedBaseCommand

from apps.utilities.factories import UtilityCategoryFactory


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory testing categories of utilities.'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, **kwargs):

        count = kwargs['count'][0]

        model = UtilityCategoryFactory._meta.model

        model._default_manager.filter().delete()

        for i in range(count):
            UtilityCategoryFactory()

        logger.debug('Made factory {0} testing categories of utilities'.format(model._default_manager.count()))
