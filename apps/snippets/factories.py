
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import AbstractTimeStampedFactory, generate_text_random_length_for_field_of_model

from apps.tags.models import Tag
from apps.opinions.factories import OpinionFactory
from apps.comments.factories import CommentFactory

from .models import Snippet


class SnippetFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Snippet

    comments_is_allowed = fuzzy.FuzzyChoice((True, False))

    @factory.lazy_attribute
    def lexer(self):
        field = Snippet._meta.get_field('lexer')
        choices = field.choices
        values_choices = tuple(zip(*choices))[0]
        return fuzzy.FuzzyChoice(values_choices).fuzz()

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')

    @factory.lazy_attribute
    def code(self):
        return generate_text_random_length_for_field_of_model(self, 'code')

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        random_count_tags = random.randint(Tag.MIN_COUNT_TAGS_ON_OBJECT, Tag.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), random_count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randrange(5)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def opinions(self, created, extracted, **kwargs):
        for i in range(random.randrange(5)):
            OpinionFactory(content_object=self)

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()
