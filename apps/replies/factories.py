
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from mylabour.factories_utils import generate_words

from .models import Reply


class ReplyFactory(factory.DjangoModelFactory):

    class Meta:
        model = Reply

    text_reply = factory.Faker('text', locale='ru')
    mark_for_language = fuzzy.FuzzyInteger(1, 5)
    mark_for_content = fuzzy.FuzzyInteger(1, 5)
    mark_for_style = fuzzy.FuzzyInteger(1, 5)

    @factory.lazy_attribute
    def user(self):
        users_given_their_replies = self.content_object.replies.values('user')
        users_given_not_their_replies = get_user_model().objects.exclude(pk__in=users_given_their_replies)
        return users_given_not_their_replies.random_users(1)

    @factory.lazy_attribute
    def impress(self):
        return factory.Faker('text', locale='ru').generate([])[:random.randint(10, 50)]

    @factory.lazy_attribute
    def advantages(self):
        return generate_words(1, 10, 'title')

    @factory.lazy_attribute
    def disadvantages(self):
        return generate_words(1, 10, 'title')

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()
        assert self.date_added >= self.user.date_joined
