
import random

import factory
from factory import fuzzy

from django.contrib.auth import get_user_model

from .models import *


Accounts = get_user_model().objects.all()


class Factory_UserComment_Generic(factory.DjangoModelFactory):

    class Meta:
        model = UserComment_Generic

    author = fuzzy.FuzzyChoice(tuple(Accounts))
    text_comment = factory.Faker('text', locale='ru')


class Factory_UserOpinion_Generic(factory.DjangoModelFactory):

    class Meta:
        model = UserOpinion_Generic

    user = fuzzy.FuzzyChoice(tuple(Accounts))
    is_useful = fuzzy.FuzzyChoice([None, True, False])

    @factory.lazy_attribute
    def is_favorite(self):
        if self.is_useful is None:
            return UserOpinion_Generic.CHOICES_FAVORITE.yes
        return fuzzy.FuzzyChoice(tuple(UserOpinion_Generic.CHOICES_FAVORITE._db_values)).fuzz()


class Factory_UserLike_Generic(factory.DjangoModelFactory):

    class Meta:
        model = UserLike_Generic

    user = fuzzy.FuzzyChoice(tuple(Accounts))
    liked_it = fuzzy.FuzzyChoice([True, False])
