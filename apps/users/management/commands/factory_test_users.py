
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import UserFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = 'Factory a given amount users.'

    def handle(self, *args, **kwargs):

        UserModel = UserFactory._meta.model

        UserModel.objects.filter().delete()

        count = kwargs['count'][0]

        for i in range(count):
            UserFactory()

        logger.debug('Made factory {} users.'.format(
            UserModel.objects.count()
        ))
