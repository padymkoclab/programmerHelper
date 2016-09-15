
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import SolutionFactory

logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = None

    def handle(self, **kwargs):

        count = kwargs['count'][0]

        SolutionModel = SolutionFactory._meta.model

        SolutionModel.objects.filter().delete()

        for i in range(count):
            SolutionFactory()

        logger.debug('Made factory {0} solutions'.format(count))
