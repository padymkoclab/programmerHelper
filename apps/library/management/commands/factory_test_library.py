
import random
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import BookFactory, WriterFactory, PublisherFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = 'Factory a passed count of books for testing.'

    def handle(self, *args, **kwargs):

        count = kwargs.get('count')[0]

        BookModel = BookFactory._meta.model
        WriterModel = WriterFactory._meta.model
        PublisherModel = PublisherFactory._meta.model

        BookModel.objects.filter().delete()
        WriterModel.objects.filter().delete()
        PublisherModel.objects.filter().delete()

        for i in range(20):
            PublisherFactory()

        for i in range(random.randint(5, 40)):
            WriterFactory()

        for i in range(count):
            BookFactory()

        logger.debug('Made factory in library: books ({}), publishers ({}), writers ({})'.format(
            BookModel.objects.count(),
            WriterModel.objects.count(),
            PublisherModel.objects.count(),
        ))
