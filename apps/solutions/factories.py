
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.generic_models.factories import Factory_CommentGeneric, Factory_OpinionGeneric

from .models import *


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
    author = fuzzy.FuzzyChoice(get_user_model().objects.all())
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
    def links(self, created, extracted, **kwargs):
        count_links = random.randint(0, WebLink.MAX_COUNT_WEBLINKS_ON_OBJECT)
        links = random.sample(tuple(WebLink.objects.all()), count_links)
        self.links.set(links)

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 3)):
            Factory_CommentGeneric(content_object=self)

    @factory.post_generation
    def opinions(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            Factory_OpinionGeneric(content_object=self)


def factory_solutions_categories():
    # import ipdb; ipdb.set_trace()
    SolutionCategory.objects.filter().delete()
    for i in range(10):
        Factory_SolutionCategory()


def factory_solutions(count):
    if not SolutionCategory.objects.count():
        factory_solutions_categories()
    for i in range(count):
        Factory_Solution(category=SolutionCategory.objects.get_random_category())


def factory_categories_of_solutions_and_solutions(count_solutions):
    factory_solutions(count_solutions)
