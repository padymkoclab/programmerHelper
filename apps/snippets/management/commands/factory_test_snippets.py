
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import SnippetFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = 'Factory test snippets'

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        SnippetModel = SnippetFactory._meta.model
        SnippetModel._default_manager.filter().delete()

        for i in range(count):
            SnippetFactory()

        logger.debug('Made factory {} snippets'.format(
            SnippetModel._default_manager.count()
        ))
