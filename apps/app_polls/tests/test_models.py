
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import *


Accounts = get_user_model().objects.all()


class Factory_Poll(factory.django.DjangoModelFactory):

    class Meta:
        model = Poll

    accessability = fuzzy.FuzzyChoice(tuple(Poll.CHOICES_ACCESSABILITY._db_values))
    status = fuzzy.FuzzyChoice(tuple(Poll.CHOICES_STATUS._db_values))

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]


class Factory_Choice(factory.django.DjangoModelFactory):

    class Meta:
        model = Choice

    poll = fuzzy.FuzzyChoice(tuple(Poll.objects.all()))
    text_choice = factory.Faker('text', locale='ru')


Poll.objects.filter().delete()
for i in range(20):
    poll = Factory_Poll()
    count_random_choices = random.randint(Poll.MIN_COUNT_CHOICES_IN_POLL, Poll.MAX_COUNT_CHOICES_IN_POLL)
    for i in range(count_random_choices):
        Factory_Choice(poll=poll)
for poll in Poll.objects.all():
    random_count_users = random.randrange(len(Accounts))
    users = random.sample(tuple(Accounts), random_count_users)
    for user in users:
        choice = random.choice(tuple(poll.choices.all()))
        VoteInPoll.objects.create(user=user, poll=poll, choice=choice)
