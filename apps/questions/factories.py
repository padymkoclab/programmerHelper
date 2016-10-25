
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import generate_text_random_length_for_field_of_model, AbstractTimeStampedFactory

from apps.tags.models import Tag
from apps.opinions.factories import OpinionFactory
from apps.comments.factories import CommentFactory

from .models import Question, Answer


class QuestionFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Question

    text_question = factory.Faker('text', locale='ru')
    status = fuzzy.FuzzyChoice([value for value, label in Question.CHOICES_STATUS])
    views = fuzzy.FuzzyInteger(1000)

    @factory.lazy_attribute
    def title(self):
        return generate_text_random_length_for_field_of_model(self, 'title')

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.lazy_attribute
    def text_question(self):
        return generate_text_random_length_for_field_of_model(self, 'text_question')

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        count_tags = random.randint(Tag.MIN_COUNT_TAGS_ON_OBJECT, Tag.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def opinions(self, create, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            OpinionFactory(content_object=self)

    @factory.post_generation
    def created(self, create, extracted, **kwargs):
        self.created = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()


class AnswerFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Answer

    @factory.lazy_attribute
    def is_accepted(self):
        if any(self.question.answers.values_list('is_accepted', flat=True)):
            return False
        return random.choice([True, False])

    @factory.lazy_attribute
    def text_answer(self):
        return generate_text_random_length_for_field_of_model(self, 'text_answer')

    @factory.lazy_attribute
    def user(self):
        users = get_user_model()._default_manager.exclude(pk__in=self.question.answers.values('user'))
        return fuzzy.FuzzyChoice(users).fuzz()

    @factory.post_generation
    def opinions(self, create, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            OpinionFactory(content_object=self)

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def created(self, create, extracted, **kwargs):
        self.created = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()
