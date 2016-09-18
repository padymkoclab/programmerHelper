
import random

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import generate_text_random_length_for_field_of_model, generate_image

from .models import Section, Forum, Topic, Post


User = get_user_model().objects.all()


class SectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Section

    position = factory.Sequence(lambda x: x + 1)

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def image(self):
        return generate_image(filename='forum_section_test.png')

    @factory.post_generation
    def groups(self, created, extracted, **kwargs):

        if not Group.objects.exists():
            raise Exception('No groups for choice')

        return random.sample(
            tuple(Group.objects.all()),
            random.randint(0, Group.objects.count())
        )


class ForumFactory(factory.DjangoModelFactory):

    class Meta:
        model = Forum

    description = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')

    @factory.post_generation
    def moderators(self, created, extracted, **kwargs):

        User = get_user_model()

        if not User._default_manager.exists():
            raise Exception('No users for choice')

        return random.sample(
            tuple(User._default_manager.all()),
            random.randint(0, User._default_manager.count())
        )


class TopicFactory(factory.DjangoModelFactory):

    class Meta:
        model = Topic

    status = fuzzy.FuzzyChoice([val for val, label in Topic.CHOICES_STATUS])
    views = fuzzy.FuzzyInteger(0, 1000)
    is_sticky = fuzzy.FuzzyChoice((True, False))
    is_closed = fuzzy.FuzzyChoice((True, False))

    @factory.lazy_attribute
    def subject(self):
        return generate_text_random_length_for_field_of_model(self, 'subject')

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()


class PostFactory(factory.DjangoModelFactory):

    class Meta:
        model = Post

    content = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()
