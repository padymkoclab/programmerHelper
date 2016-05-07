
import random

import factory
from factory import fuzzy

from .models import *


class Factory_TestSuit(factory.DjangoModelFactory):

    class Meta:
        model = TestSuit

    description = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(Account.objects.all())
    complexity = fuzzy.FuzzyChoice(tuple(TestSuit.CHOICES_COMPLEXITY._db_values))

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


class Factory_TestPassageUser(factory.django.DjangoModelFactory):

    class Meta:
        model = TestPassageUser

    user = fuzzy.FuzzyChoice(Account.objects.all())
    test_suit = fuzzy.FuzzyChoice(Account.objects.all())
    status = fuzzy.FuzzyChoice(TestPassageUser.CHOICES_STATUS._db_values)
    scope = fuzzy.FuzzyInteger(TestPassageUser.MIN_SCOPE, TestPassageUser.MAX_SCOPE)


class Factory_TestQuestion(factory.DjangoModelFactory):

    class Meta:
        model = TestQuestion

    test_suit = fuzzy.FuzzyChoice(TestSuit.objects.all())
    text_question = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:40]


class Factory_Variant(factory.DjangoModelFactory):

    class Meta:
        model = Variant

    question = fuzzy.FuzzyChoice(TestQuestion.objects.all())
    text_variant = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def is_right_variant(self):
        is_right_variant = True
        if self.question.have_one_right_variant():
            return False
        return is_right_variant


TestSuit.objects.filter().delete()
for i in range(10):
    test_suit = Factory_TestSuit()
    for k in range(20):
        user = random.choice(tuple(Account.objects.all()))
        Factory_TestPassageUser(user=user, test_suit=test_suit)
    for j in range(TestSuit.MIN_COUNT_QUESTIONS, TestSuit.MAX_COUNT_QUESTIONS):
        question = Factory_TestQuestion(test_suit=test_suit)
        for e in range(TestQuestion.MIN_COUNT_VARIANTS, TestQuestion.MAX_COUNT_VARIANTS):
            Factory_Variant(question=question)
