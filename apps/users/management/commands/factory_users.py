
import random
import logging

from django.contrib.auth.models import Group
from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import UserFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = 'Factory a given amount users.'

    def handle(self, *args, **kwargs):

        UserModel = UserFactory._meta.model

        UserModel._default_manager.filter().delete()

        group_moderators = Group.objects.get(name='moderators')
        group_banned = Group.objects.get(name='banned')

        count = kwargs['count'][0]

        for i in range(count):

            number = random.random()
            user = UserFactory()

            if number > .9:
                user.groups.add(group_moderators)
            elif number < .1:
                user.groups.add(group_banned)

        logger.info('Made factory {} users.'.format(UserModel.objects.count()))
