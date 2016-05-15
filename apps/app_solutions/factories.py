
import random

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_CommentGeneric, Factory_OpinionGeneric

from .models import *


Accounts = Account.objects.all()


class Factory_SolutionCategory(factory.DjangoModelFactory):

    class Meta:
        model = SolutionCategory

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def description(self):
        return factory.Faker('text', locale='ru').generate([])

    @factory.lazy_attribute
    def lexer(self):
        return random.choice(CHOICES_LEXERS)[0]


class Factory_Solution(factory.DjangoModelFactory):

    class Meta:
        model = Solution

    category = fuzzy.FuzzyChoice(SolutionCategory.objects.all())
    author = fuzzy.FuzzyChoice(Account.objects.all())
    views = fuzzy.FuzzyInteger(1000)

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def body(self):
        text_body = str()
        for i in range(3):
            text_body += factory.Faker('text', locale='ru').generate([])
        return text_body

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randint(Tag.MIN_COUNT_TAGS_ON_OBJECT, Tag.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def useful_links(self, created, extracted, **kwargs):
        count_useful_links = random.randint(0, WebLink.MAX_COUNT_WEBLINKS_ON_OBJECT)
        useful_links = random.sample(tuple(WebLink.objects.all()), count_useful_links)
        self.useful_links.set(useful_links)

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 3)):
            Factory_CommentGeneric(content_object=self)

    @factory.post_generation
    def opinions(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            Factory_OpinionGeneric(content_object=self)


SolutionCategory.objects.filter().delete()
for i in range(10):
    category = Factory_SolutionCategory()
    for j in range(random.randrange(8)):
        solution = Factory_Solution(category=category)
