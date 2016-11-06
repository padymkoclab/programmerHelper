
import random

from django.utils import timezone
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import (
    generate_text_random_length_for_field_of_model,
    AbstractTimeStampedFactory,
)

from .models import Section, Forum, Topic, Post


NOW = timezone.now()


class SectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Section

    position = factory.Sequence(lambda x: x + 1)

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

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

    @factory.post_generation
    def created(self, created, extracted, **kwargs):
        self.created = fuzzy.FuzzyDateTime(NOW - timezone.timedelta(days=500)).fuzz()
        self.save()


class TopicFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Topic

    count_views = fuzzy.FuzzyInteger(0, 1000)
    is_sticky = fuzzy.FuzzyChoice((True, False))
    is_opened = fuzzy.FuzzyChoice((True, False))

    @factory.lazy_attribute
    def subject(self):
        return generate_text_random_length_for_field_of_model(self, 'subject')

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.post_generation
    def created(self, created, extracted, **kwargs):

        min_created = max(self.user.date_joined, self.forum.created)
        self.created = fuzzy.FuzzyDateTime(min_created).fuzz()
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
    def created(self, created, extracted, **kwargs):

        min_created = max(self.user.date_joined, self.topic.created)
        self.created = fuzzy.FuzzyDateTime(min_created).fuzz()
        self.save()
