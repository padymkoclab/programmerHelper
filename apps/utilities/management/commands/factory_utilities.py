

import logging

from utils.django.basecommands import FactoryCountBaseCommand

from apps.utilities.factories import CategoryFactory, UtilityFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = 'Factory testing categories with utilities.'

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
