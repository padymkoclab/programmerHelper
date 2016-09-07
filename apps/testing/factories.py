
import random

from django.contrib.auth import get_user_model
from django.utils import timezone

import factory
from factory import fuzzy

from utils.django.factories_utils import (
    generate_image,
    generate_text_random_length_for_field_of_model,
    AbstractTimeStampedFactory
)

from .models import Suit, Passage, TestQuestion, Variant


User = get_user_model()


class SuitFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Suit

    complexity = fuzzy.FuzzyChoice([choice for choice, label in Suit.CHOICES_COMPLEXITY])
    status = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def image(self):
        return generate_image(filename='Testing suit')

    @factory.lazy_attribute
    def duration(self):

        for validators in Suit._meta.get_field('duration').validators:
            if validators.code == 'min_value':
                min_value = validators.limit_value.total_seconds()
            elif validators.code == 'max_value':
                max_value = validators.limit_value.total_seconds()

        seconds = random.randint(min_value, max_value)
        return timezone.timedelta(seconds=seconds)

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')


class TestQuestionFactory(AbstractTimeStampedFactory):

    class Meta:
        model = TestQuestion

    @factory.lazy_attribute
    def title(self):
        return generate_text_random_length_for_field_of_model(self, 'title')

    @factory.lazy_attribute
    def text_question(self):
        return generate_text_random_length_for_field_of_model(self, 'text_question')

    @factory.lazy_attribute
    def suit(self):
        if not Suit.objects.count():
            raise ValueError('Does not exists suits at all.')
        return fuzzy.FuzzyChoice(Suit.objects.all()).fuzz()

    @factory.post_generation
    def date_added(self, create, extracted, **kwargs):
        # a question may added only after a suit was created
        new_date = fuzzy.FuzzyDateTime(self.suit.date_added).fuzz()
        self.date_added = new_date
        self.save()


class VariantFactory(factory.DjangoModelFactory):

    class Meta:
        model = Variant

    @factory.lazy_attribute
    def question(self):
        if not TestQuestion.objects.count():
            raise ValueError('Does not exists questions at all.')
        return fuzzy.FuzzyChoice(TestQuestion.objects.all()).fuzz()

    @factory.lazy_attribute
    def text_variant(self):
        return generate_text_random_length_for_field_of_model(self, 'text_variant')

    @factory.lazy_attribute
    def is_right_variant(self):
        return random.choice([True, False])


class PassageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Passage

    status = fuzzy.FuzzyChoice([choice for choice, label in Passage.CHOICES_STATUS])
    mark = fuzzy.FuzzyInteger(Passage.MIN_MARK, Passage.MAX_MARK)

    @factory.lazy_attribute
    def user(self):
        if not User.objects.count():
            raise ValueError('Does not exists users at all.')
        return fuzzy.FuzzyChoice(User.objects.all()).fuzz()

    @factory.lazy_attribute
    def suit(self):
        if not Suit.objects.count():
            raise ValueError('Does not exists suits at all.')
        return fuzzy.FuzzyChoice(Suit.objects.all()).fuzz()

    @factory.post_generation
    def date_passage(self, create, extracted, **kwargs):
        # a passage could happen  only after a suit was created and an user existed
        min_possible_date = max(self.user.date_joined, self.suit.date_added)
        new_date = fuzzy.FuzzyDateTime(min_possible_date).fuzz()
        self.date_passage = new_date
        self.save()
