
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import AbstractTimeStampedFactory

from .models import Flavour


class FlavourFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Flavour

    status = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def user(self):
        already_given_his_flavours_users = self.content_object.flavours.values('user')
        author_labour = self.content_object.user
        users_yet_not_his_flavours = get_user_model().objects.exclude(pk__in=already_given_his_flavours_users)
        users_yet_not_his_flavours_and_no_author = users_yet_not_his_flavours.exclude(pk=author_labour.pk)
        if not users_yet_not_his_flavours_and_no_author.count():
            msg = 'All users already given his favour about {0} "{1}"'.format(
                self.content_object._meta.verbose_name.lower(),
                self.content_object.__str__()
            )
            raise ValueError(msg)
        return users_yet_not_his_flavours_and_no_author.random_users(1)
