
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from mylabour.utils import generate_text_by_min_length

from .models import *


class PollFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Poll

    status = fuzzy.FuzzyChoice(Poll.CHOICES_STATUS._db_values)

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def description(self):
        return generate_text_by_min_length(50)[:100]


class ChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Choice

    poll = fuzzy.FuzzyChoice(Poll.objects.opened_polls())
    text_choice = factory.Faker('text', locale='ru')


def polls_factory(count):
    Accounts = get_user_model().objects.all()
    Poll.objects.filter().delete()
    # create polls
    for i in range(count):
        poll = PollFactory()
        # create and add choices for poll
        count_random_choices = random.randint(Poll.MIN_COUNT_CHOICES_IN_POLL, Poll.MAX_COUNT_CHOICES_IN_POLL)
        for i in range(count_random_choices):
            ChoiceFactory(poll=poll)
        # added votes with unique accounts
        random_count_users = random.randrange(len(Accounts))
        accounts = random.sample(tuple(Accounts), random_count_users)
        for account in accounts:
            choice = random.choice(tuple(poll.choices.all()))
            VoteInPoll.objects.create(account=account, poll=poll, choice=choice)
