
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_OpinionGeneric, Factory_CommentGeneric

from .models import *


Accounts = get_user_model().objects.all()


class Factory_Snippet(factory.DjangoModelFactory):

    class Meta:
        model = Snippet

    author = fuzzy.FuzzyChoice(Accounts)
    description = factory.Faker('text', locale='ru')
    code = factory.Faker('text', locale='en')
    views = fuzzy.FuzzyInteger(1000)

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
            Factory_CommentGeneric(content_object=self)

    @factory.post_generation
    def opinions(self, created, extracted, **kwargs):
        for i in range(random.randrange(5)):
            Factory_OpinionGeneric(content_object=self)


Snippet.objects.filter().delete()
for i in range(50):
    Factory_Snippet()
