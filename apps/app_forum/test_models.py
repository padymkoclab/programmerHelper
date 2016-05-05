
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import *


User_model = get_user_model()


class Factory_TopicCategory(factory.DjangoModelFactory):

    class Meta:
        model = TopicCategory

    description = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:50]


class Factory_Topic(factory.DjangoModelFactory):

    class Meta:
        model = Topic

    description = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(User_model.objects.filter(is_superuser=True, is_active=True))
    category = fuzzy.FuzzyChoice(TopicCategory.objects.all())

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def status(self):
        return random.choice(Topic.STATUS_CHOICES)[0]


class Factory_Post(factory.DjangoModelFactory):

    class Meta:
        model = Post

    content = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(User_model.objects.all())
    topic = fuzzy.FuzzyChoice(Topic.objects.all())
