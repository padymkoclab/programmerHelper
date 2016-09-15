
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import NewsletterFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        NewsletterModel = NewsletterFactory._meta.model
        NewsletterModel.objects.filter().delete()

        for i in range(count):

            NewsletterFactory()

        logger.debug('Cleared all newsletters')
        logger.debug('Made factory {} newsletters'.format(
            NewsletterModel.objects.count()
        ))
