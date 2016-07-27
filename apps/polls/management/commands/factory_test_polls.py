
import random

from django.contrib.auth import get_user_model


from mylabour.utils import get_random_date_from_days_ago_to_now
from mylabour.basecommands import ExtendedBaseCommand
from mylabour.utils import create_logger_by_filename

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll, Choice, VoteInPoll


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory a given amount of polls, include choices and votes.'

    def add_arguments(self, parser):
        parser.add_argument('count_polls', nargs=1, type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):
        count_polls = kwargs['count_polls'][0]

        # get access to user`s model
        Accounts = get_user_model().objects.all()

        # delete all polls, choices, votes
        Poll.objects.filter().delete()

        # create polls
        for i in range(count_polls):
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

        logger.debug('Made factory polls ({0}), choices ({1}) and votes ({2}).'.format(
            Poll.objects.count(),
            Choice.objects.count(),
            VoteInPoll.objects.count(),
        ))

        self._shuffle_dates()
        logger.debug('Shuffled dates in objects')

    def _shuffle_dates(self):
        """ """

        for poll in Poll.objects.all().prefetch_related('voteinpoll_set'):

            # change date_added
            new_date_added = get_random_date_from_days_ago_to_now()
            Poll.objects.filter(pk=poll.pk).update(date_added=new_date_added)

            # change date_modified given that it must be more or equal date_added
            new_date_modified = get_random_date_from_days_ago_to_now(new_date_added)
            Poll.objects.filter(pk=poll.pk).update(date_modified=new_date_modified)

            for vote in poll.voteinpoll_set.iterator():
                new_date_voting = get_random_date_from_days_ago_to_now(new_date_added)
                poll.voteinpoll_set.filter(pk=vote.pk).update(date_voting=new_date_voting)
