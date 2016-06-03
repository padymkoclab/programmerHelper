
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.opinions.factories import OpinionFactory
from apps.comments.factories import CommentFactory
from apps.favours.factories import FavourFactory

from .models import *


class SnippetFactory(factory.DjangoModelFactory):

    class Meta:
        model = Snippet

    account = fuzzy.FuzzyChoice(get_user_model().objects.all())
    description = factory.Faker('text', locale='ru')
    code = factory.Faker('text', locale='en')

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def lexer(self):
        return random.choice(CHOICES_LEXERS)[0]

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        random_count_tags = random.randint(Tag.MIN_COUNT_TAGS_ON_OBJECT, Tag.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), random_count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randrange(3)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def opinions(self, created, extracted, **kwargs):
        for i in range(random.randrange(5)):
            OpinionFactory(content_object=self)

    @factory.post_generation
    def favours(self, created, extracted, **kwargs):
        for i in range(random.randrange(5)):
            FavourFactory(content_object=self)


def snippets_factory(count):
    Snippet.objects.filter().delete()
    for i in range(count):
        SnippetFactory()
