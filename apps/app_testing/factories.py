
import random

import factory
from factory import fuzzy

from .models import *


class Factory_TestingSuit(factory.DjangoModelFactory):

    class Meta:
        model = TestingSuit

    description = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(Account.objects.all())
    complexity = fuzzy.FuzzyChoice(tuple(TestingSuit.CHOICES_COMPLEXITY._db_values))

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def picture(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        image_slug_name = factory.Faker('slug', locale='ru').generate([])
        return site_name + image_slug_name + '.jpg'

    @factory.lazy_attribute
    def duration(self):
        duration = factory.Faker('time', locale='ru').generate([])
        return '00' + duration[2:]


class Factory_TestingPassage(factory.django.DjangoModelFactory):

    class Meta:
        model = TestingPassage

    user = fuzzy.FuzzyChoice(Account.objects.all())
    test_suit = fuzzy.FuzzyChoice(TestingSuit.objects.all())
    status = fuzzy.FuzzyChoice(TestingPassage.CHOICES_STATUS._db_values)
    scope = fuzzy.FuzzyInteger(TestingPassage.MIN_SCOPE, TestingPassage.MAX_SCOPE)


class Factory_TestingQuestion(factory.DjangoModelFactory):

    class Meta:
        model = TestingQuestion

    test_suit = fuzzy.FuzzyChoice(TestingSuit.objects.all())
    text_question = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:40]


class Factory_TestingVariant(factory.DjangoModelFactory):

    class Meta:
        model = TestingVariant

    question = fuzzy.FuzzyChoice(TestingQuestion.objects.all())
    text_variant = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def is_right_variant(self):
        if self.question.have_one_right_variant():
            return False
        return random.choice([True, False])


TestingSuit.objects.filter().delete()
for i in range(10):
    test_suit = Factory_TestingSuit()
    for j in range(random.randrange(30)):
        Factory_TestingPassage(test_suit=test_suit)
    for h in range(random.randint(TestingSuit.MIN_COUNT_QUESTIONS, TestingSuit.MAX_COUNT_QUESTIONS)):
        question = Factory_TestingQuestion(test_suit=test_suit)
        for g in range(random.randint(TestingQuestion.MIN_COUNT_VARIANTS, TestingQuestion.MAX_COUNT_VARIANTS)):
            Factory_TestingVariant(question=question)
