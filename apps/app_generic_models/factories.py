
import random

import factory
from factory import fuzzy

from django.contrib.auth import get_user_model

from .models import *
from .exceptions import UniqueAccountDepletedError


def get_unique_user(instance, excluded_pks, counter=0):
    Accounts = get_user_model().objects.exclude(pk__in=excluded_pks)
    account = random.choice(Accounts)
    try:
        instance.user = account
        instance.author = account
        instance.full_clean()
    except:
        if counter == len(Accounts):
            raise UniqueAccountDepletedError('Accounts depleted.')
        counter += 1
        return get_unique_user(instance, excluded_pks, counter)
    else:
        return account


class Factory_CommentGeneric(factory.DjangoModelFactory):

    class Meta:
        model = CommentGeneric

    text_comment = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(get_user_model().objects.all())


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
        if hasattr(self.content_object, 'author'):
            excluded_pks = [self.content_object.author.pk]
        elif hasattr(self.content_object, 'user'):
            excluded_pks = [self.content_object.user.pk]
        elif hasattr(self.content_object, 'authorship'):
            excluded_pks = self.content_object.authorship.values_list('pk', flat=True)
        else:
            raise Exception()
        return get_unique_user(instance, excluded_pks)


class Factory_LikeGeneric(factory.DjangoModelFactory):

    class Meta:
        model = LikeGeneric

    liked_it = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def user(self):
        instance = LikeGeneric(content_object=self.content_object, liked_it=self.liked_it)
        if hasattr(self.content_object, 'author'):
            excluded_pks = [self.content_object.author.pk]
        elif hasattr(self.content_object, 'user'):
            excluded_pks = [self.content_object.user.pk]
        elif hasattr(self.content_object, 'authorship'):
            excluded_pks = self.content_object.authorship.values_list('pk', flat=True)
        else:
            raise Exception()
        return get_unique_user(instance, excluded_pks)


class Factory_ScopeGeneric(factory.DjangoModelFactory):

    class Meta:
        model = ScopeGeneric

    @factory.lazy_attribute
    def scope(self):
        return random.randint(ScopeGeneric.MIN_SCOPE, ScopeGeneric.MAX_SCOPE)

    @factory.lazy_attribute
    def user(self):
        instance = ScopeGeneric(content_object=self.content_object, scope=self.scope)
        if hasattr(self.content_object, 'author'):
            excluded_pks = [self.content_object.author.pk]
        elif hasattr(self.content_object, 'user'):
            excluded_pks = [self.content_object.user.pk]
        elif hasattr(self.content_object, 'authorship'):
            excluded_pks = self.content_object.authorship.values_list('pk', flat=True)
        else:
            import ipdb; ipdb.set_trace()
            raise Exception()
        return get_unique_user(instance, excluded_pks)
