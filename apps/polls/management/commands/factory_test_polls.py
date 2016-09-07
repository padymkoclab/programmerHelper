
import random

from django.contrib.auth import get_user_model

from utils.django.datetime_utils import get_random_date_from_days_ago_to_now
from utils.django.basecommands import ExtendedBaseCommand
from utils.python.logging_utils import create_logger_by_filename

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll, Choice, Vote
from apps.polls.constants import MIN_COUNT_CHOICES_IN_POLL, MAX_COUNT_CHOICES_IN_POLL


# get access to user`s model
User = get_user_model()

logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory a given amount of polls, include choices and votes.'

    def add_arguments(self, parser):
        parser.add_argument('count_polls', nargs=1, type=self._positive_integer_from_1_to_999)

        parser.add_argument(
            '--without-votes',
            action='store_true',
            dest='without-votes',
            default=False,
            help='Creating polls and choices without votes.'
        )

    def handle(self, *args, **kwargs):
        count_polls = kwargs['count_polls'][0]

        # delete all polls, choices, votes
        Poll.objects.filter().delete()

        # create polls
        polls = set()
        for i in range(count_polls):
            poll = PollFactory.build()
            polls.add(poll)
        Poll.objects.bulk_create(polls)

        # create choices for an each poll
        choices = set()
        for poll in polls:
            count_random_choices = random.randint(
                MIN_COUNT_CHOICES_IN_POLL,
                MAX_COUNT_CHOICES_IN_POLL
            )
            for i in range(count_random_choices):
                choice = ChoiceFactory.build(poll=poll)
                choices.add(choice)
        Choice.objects.bulk_create(choices)

        # if needed, creating votes
        if not kwargs['without-votes']:

            # check up an existence of users
            count_users = User.objects.count()
            assert count_users > 0, 'Not users for voting'

            # create votes, where unique user and poll
            votes = set()
            for poll in polls:
                random_count_users = random.randint(0, count_users)
                users = User.objects.random_users(random_count_users, True)
                for user in users:
                    choice = random.choice(tuple(poll.choices.all()))
                    vote = Vote(user=user, poll=poll, choice=choice)
                    votes.add(vote)
            Vote.objects.bulk_create(votes)

        # make a report
        logger.debug('Made factory polls ({0}), choices ({1}) and votes ({2}).'.format(
            Poll.objects.count(),
            Choice.objects.count(),
            Vote.objects.count(),
        ))

        # make shuffle a dates in newly-created objects
        self._shuffle_dates()

        logger.debug('Shuffled dates in objects')

    def _shuffle_dates(self):
        """ """

        for poll in Poll.objects.prefetch_related('voters', 'choices', 'votes'):

            # change dates added of polls
            new_date_added = get_random_date_from_days_ago_to_now()
            Poll.objects.filter(pk=poll.pk).update(date_added=new_date_added)

            # change date modified of choices
            # given that it must be more or equal date_added
            new_date_modified = get_random_date_from_days_ago_to_now(new_date_added)
            Poll.objects.filter(pk=poll.pk).update(date_modified=new_date_modified)

            # change dates of voting in votes
            # given that it must be more than date added of a corresponding poll
            for vote in poll.votes.iterator():
                new_date_voting = get_random_date_from_days_ago_to_now(new_date_added)
                poll.votes.filter(pk=vote.pk).update(date_voting=new_date_voting)
