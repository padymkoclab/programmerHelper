
import random

import factory
from factory import fuzzy

from django.contrib.auth import get_user_model

from .models import *


Accounts = get_user_model().objects.all()


class Factory_CommentGeneric(factory.DjangoModelFactory):

    class Meta:
        model = CommentGeneric

    author = fuzzy.FuzzyChoice(tuple(Accounts))
    text_comment = factory.Faker('text', locale='ru')


class Factory_OpinionGeneric(factory.DjangoModelFactory):

    class Meta:
        model = OpinionGeneric

    user = fuzzy.FuzzyChoice(tuple(Accounts))
    is_useful = fuzzy.FuzzyChoice([None, True, False])

    @factory.lazy_attribute
    def is_favorite(self):
        choices = [True, False, None]
        if self.is_useful is None:
            choices = [True, False]
        return random.choice(choices)


class Factory_LikeGeneric(factory.DjangoModelFactory):

    class Meta:
        model = LikeGeneric

    user = fuzzy.FuzzyChoice(tuple(Accounts))
    liked_it = fuzzy.FuzzyChoice([True, False])


class Factory_ScopeGeneric(factory.DjangoModelFactory):

    class Meta:
        model = ScopeGeneric

    user = fuzzy.FuzzyChoice(tuple(Accounts))

    @factory.lazy_attribute
    def scope(self):
        return random.randint(ScopeGeneric.MIN_SCOPE, ScopeGeneric.MAX_SCOPE)
