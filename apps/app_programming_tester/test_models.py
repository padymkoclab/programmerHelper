
import random
import factory
from factory import fuzzy

from .models import *


class Factory_TestSuit(factory.DjangoModelFactory):

    class Meta:
        model = TestSuit

    description = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(Account.objects.all())
    count_attempts_passing = fuzzy.FuzzyInteger(10)
    count_completed_passing = fuzzy.FuzzyInteger(10)
    complexity = fuzzy.FuzzyChoice(list(i[0] for i in TestSuit.CHOICES_COMPLEXITY))

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def image_url(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        image_slug_name = factory.Faker('slug', locale='ru').generate([])
        return site_name + image_slug_name + '.jpg'

    @factory.lazy_attribute
    def duration(self):
        duration = factory.Faker('time', locale='ru').generate([])
        return '00' + duration[2:]


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
