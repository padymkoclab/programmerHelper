
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_OpinionGeneric, Factory_CommentGeneric, Factory_LikeGeneric

from .models import *

Accounts = get_user_model().objects.all()


class Factory_Question(factory.DjangoModelFactory):

    class Meta:
        model = Question

    text_question = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(tuple(Accounts))
    status = fuzzy.FuzzyChoice(tuple(Question.CHOICES_STATUS._db_values))
    views = fuzzy.FuzzyInteger(1000)

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def is_dublicated(self):
        if divmod(random.random(), 0.1)[0] > 8:
            return True
        return False

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        count_tags = random.randint(Tag.MIN_COUNT_TAGS_ON_OBJECT, Tag.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def opinions(self, create, extracted, **kwargs):
        for i in range(random.randrange(10)):
            Factory_OpinionGeneric(content_object=self)

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        for i in range(random.randrange(10)):
            Factory_CommentGeneric(content_object=self)


Question.objects.filter().delete()
for i in range(100):
    Factory_Question()


class Factory_Answer(factory.DjangoModelFactory):

    class Meta:
        model = Answer

    text_answer = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(tuple(Accounts))
    question = fuzzy.FuzzyChoice(tuple(Question.objects.all()))

    @factory.lazy_attribute
    def is_acceptabled(self):
        if self.question.has_acceptable_answer():
            return False
        return random.choice([True, False])

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        for i in range(random.randrange(10)):
            Factory_LikeGeneric(content_object=self)

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        for i in range(random.randrange(10)):
            Factory_CommentGeneric(content_object=self)


for j in range(300):
    Factory_Answer()
