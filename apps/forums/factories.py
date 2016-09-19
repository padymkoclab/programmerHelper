
import random

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import (
    generate_text_random_length_for_field_of_model,
    generate_image,
    AbstractTimeStampedFactory,
)

from .models import Section, Forum, Topic, Post


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


class ForumFactory(AbstractTimeStampedFactory):

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


class TopicFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Topic

    views = fuzzy.FuzzyInteger(0, 1000)
    is_sticky = fuzzy.FuzzyChoice((True, False))
    is_opened = fuzzy.FuzzyChoice((True, False))

    @factory.lazy_attribute
    def subject(self):
        return generate_text_random_length_for_field_of_model(self, 'subject')

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()


class PostFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Post

    markup = fuzzy.FuzzyChoice([val for val, label in Post._meta.get_field('markup').choices])

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.lazy_attribute
    def content(self):
        return generate_text_random_length_for_field_of_model(self, 'content')

    @factory.lazy_attribute
    def user_ip(self):
        if random.random() > .5:
            return factory.Faker('ipv6').generate([])
        return factory.Faker('ipv4').generate([])

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):

        count_posts = self.topic.posts.count()

        # if is not a head of the topic
        if count_posts != 1:
            self.date_added = fuzzy.FuzzyDateTime(self.topic.date_added).fuzz()

        self.save()
