
from utils.python.logging_utils import create_logger_by_filename
from utils.django.basecommands import ExtendedBaseCommand

from apps.utilities.factories import CategoryFactory, UtilityFactory


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory testing categories with utilities.'

    def add_arguments(self, parser):

        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, **kwargs):

        count = kwargs['count'][0]

        CategoryModel = CategoryFactory._meta.model
        UtilityModel = UtilityFactory._meta.model

        CategoryModel.objects.filter().delete()

        for i in range(20):
            CategoryFactory()

        for i in range(count):
            UtilityFactory()

        logger.debug('Made factory testing {0} categories and {1} utilities'.format(
            CategoryModel.objects.count(),
            UtilityModel.objects.count(),
        ))
