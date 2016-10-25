
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import ArticleFactory
from ...models import Subsection, Mark


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        ArticleModel = ArticleFactory._meta.model

        ArticleModel._default_manager.filter().delete()

        for i in range(count):
            ArticleFactory()

        logger.debug('Made factory {} articles, {} subsections, {} marks.'.format(
            ArticleModel._default_manager.count(),
            Subsection._default_manager.count(),
            Mark._default_manager.count(),
        ))
