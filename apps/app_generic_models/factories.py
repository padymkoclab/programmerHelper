
import random

import factory
from factory import fuzzy

from django.contrib.auth import get_user_model

from .models import *

Accounts = get_user_model().objects.all()


def get_unique_user(instance, counter=0):
    account = random.choice(Accounts)
    try:
        instance.user = account
        instance.author = account
        instance.full_clean()
    except:
        if counter == len(Accounts):
            raise Exception('Accounts depleted.')
        counter += 1
        return get_unique_user(instance, counter)
    else:
        return account


class Factory_CommentGeneric(factory.DjangoModelFactory):

    class Meta:
        model = CommentGeneric

    text_comment = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def author(self):
        instance = CommentGeneric(content_object=self.content_object, text_comment=self.text_comment)
        return get_unique_user(instance)


class Factory_OpinionGeneric(factory.DjangoModelFactory):

    class Meta:
        model = OpinionGeneric

    is_useful = fuzzy.FuzzyChoice([None, True, False])

    @factory.lazy_attribute
    def is_favorite(self):
        choices = [True, False, None]
        if self.is_useful is None:
            choices = [True, False]
        return random.choice(choices)

    @factory.lazy_attribute
    def user(self):
        instance = OpinionGeneric(content_object=self.content_object, is_useful=self.is_useful, is_favorite=self.is_favorite)
        return get_unique_user(instance)


class Factory_LikeGeneric(factory.DjangoModelFactory):

    class Meta:
        model = LikeGeneric

    liked_it = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def user(self):
        instance = LikeGeneric(content_object=self.content_object, liked_it=self.liked_it)
        return get_unique_user(instance)


class Factory_ScopeGeneric(factory.DjangoModelFactory):

    class Meta:
        model = ScopeGeneric

    @factory.lazy_attribute
    def scope(self):
        return random.randint(ScopeGeneric.MIN_SCOPE, ScopeGeneric.MAX_SCOPE)

    @factory.lazy_attribute
    def user(self):
        instance = ScopeGeneric(content_object=self.content_object, scope=self.scope)
        return get_unique_user(instance)
