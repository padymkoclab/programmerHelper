
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import OpinionUserModel


USER_MODEL = get_user_model()


class Factory_OpinionUserModel(factory.django.DjangoModelFactory):

    is_useful = fuzzy.FuzzyChoice([True, False, None])

    @factory.lazy_attribute
    def is_favorite(self):
        if self.is_useful is None:
            return OpinionUserModel.CHOICES_FAVORITE.yes
        return random.choice(tuple(OpinionUserModel.CHOICES_FAVORITE._db_values))


class Factory_Comment(factory.django.DjangoModelFactory):

    content = factory.Faker('text', locale='ru')
