
import logging
import random

from django.contrib.auth import get_user_model

from factory import fuzzy

from utils.django.basecommands import ExtendedBaseCommand

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll, Choice, Vote
from apps.polls.constants import MIN_COUNT_CHOICES_IN_POLL, MAX_COUNT_CHOICES_IN_POLL


User = get_user_model()
logger = logging.getLogger(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory a given amount of polls, include choices and votes.'

    def add_arguments(self, parser):

        parser.add_argument('count_polls', nargs=1, type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):

        count_polls = kwargs['count_polls'][0]

        Poll.objects.filter().delete()

        users = User._default_manager.all()
        count_users = users.count()

        for i in range(count_polls):
            poll = PollFactory()

            count_random_choices = random.randint(
                MIN_COUNT_CHOICES_IN_POLL,
                MAX_COUNT_CHOICES_IN_POLL
            )
            for i in range(count_random_choices):
                choice = ChoiceFactory(poll=poll)

            random_count_users = random.randint(0, count_users)
            for user in random.sample(tuple(users), random_count_users):
                choice = random.choice(poll.choices.all())
                vote = Vote.objects.create(user=user, poll=poll, choice=choice)

                # change date voting on random
                min_date_voting = max(poll.date_added, vote.user.date_joined)
                random_date_voting = fuzzy.FuzzyDateTime(min_date_voting).fuzz()
                Vote.objects.filter(pk=vote.pk).update(date_voting=random_date_voting)

        logger.info('Made factory polls ({0}), choices ({1}) and votes ({2}).'.format(
            Poll.objects.count(),
            Choice.objects.count(),
            Vote.objects.count(),
        ))
