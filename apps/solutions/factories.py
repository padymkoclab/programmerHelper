
import random

from django.contrib.auth import get_user_model
from django.conf import settings

import factory
from factory import fuzzy

from utils.django.factories_utils import AbstractTimeStampedFactory, generate_text_random_length_for_field_of_model

from apps.tags.models import Tag
from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory

from .models import Solution


class SolutionFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Solution

    comments_is_allowed = fuzzy.FuzzyChoice((True, False))

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.lazy_attribute
    def problem(self):
        return generate_text_random_length_for_field_of_model(self, 'problem')

    @factory.lazy_attribute
    def body(self):
        return generate_text_random_length_for_field_of_model(self, 'body')

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randint(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def opinions(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            OpinionFactory(content_object=self)

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()
