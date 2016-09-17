
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import ArticleFactory, SubsectionFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        ArticleModel = ArticleFactory._meta.model
        SubsectionModel = SubsectionFactory._meta.model

        ArticleModel._default_manager.filter().delete()

        for i in range(count):
            ArticleFactory()

        logger.debug('Made factory {} articles with {} subsections'.format(
            ArticleModel._default_manager.count(),
            SubsectionModel._default_manager.count(),
        ))
