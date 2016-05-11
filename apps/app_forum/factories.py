
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import *


Accounts = get_user_model().objects.all()


class Factory_ForumSection(factory.DjangoModelFactory):

    class Meta:
        model = ForumSection

    description = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:50]


class Factory_ForumTopic(factory.DjangoModelFactory):

    class Meta:
        model = ForumTopic

    description = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(Accounts)
    views = fuzzy.FuzzyInteger(1000)

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def status(self):
        return random.choice(tuple(ForumTopic.CHOICES_STATUS._db_values))


class Factory_ForumPost(factory.DjangoModelFactory):

    class Meta:
        model = ForumPost

    content = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(Accounts)


ForumSection.objects.filter().delete()
for i in range(10):
    theme = Factory_ForumSection()
    for j in range(random.randrange(1, 20)):
        topic = Factory_ForumTopic(theme=theme)
        for e in range(random.randrange(1, 10)):
            Factory_ForumPost(topic=topic)
