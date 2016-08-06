
import random

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import TestCase

import pytest

from apps.users.factories import UserFactory

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll, Choice, Vote


User = get_user_model()


class PollQuerySetTest(TestCase):
    """
    Tests for queryset of polls.
    """

    @classmethod
    def setUpTestData(cls):

        # create users
        for i in range(30):
            UserFactory()

        cls.user1, cls.user2, cls.user3, cls.user4, cls.user5 = User.objects.all()[:5]

    def setUp(self):

        # create polls
        self.poll1 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        self.poll2 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.poll3 = PollFactory(status=Poll.CHOICES_STATUS.draft)
        self.poll4 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.poll5 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        self.poll6 = PollFactory(status=Poll.CHOICES_STATUS.draft)
        self.poll7 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.poll8 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        self.poll9 = PollFactory(status=Poll.CHOICES_STATUS.closed)

        # create choices for polls
        for poll, count_choices in (
            (self.poll1, 8),
            (self.poll2, 2),
            (self.poll3, 3),
            (self.poll4, 4),
            (self.poll5, 4),
            (self.poll6, 2),
            (self.poll7, 3),
            (self.poll8, 5),
            (self.poll9, 7),
        ):
            for i in range(count_choices):
                ChoiceFactory(poll=poll)

    def test_closed_polls_if_exists_no_closed_polls(self):

        Poll.objects.filter().delete()

        PollFactory(status='opened')
        PollFactory(status='opened')
        PollFactory(status='draft')
        PollFactory(status='draft')

        self.assertFalse(Poll.objects.closed_polls().exists())

    def test_opened_polls_if_exists_no_opened_polls(self):

        Poll.objects.filter().delete()

        PollFactory(status='closed')
        PollFactory(status='closed')
        PollFactory(status='draft')
        PollFactory(status='draft')

        self.assertFalse(Poll.objects.opened_polls().exists())

    def test_draft_polls_if_exists_no_draft_polls(self):

        Poll.objects.filter().delete()

        PollFactory(status='closed')
        PollFactory(status='opened')
        PollFactory(status='opened')
        PollFactory(status='closed')

        self.assertFalse(Poll.objects.draft_polls().exists())

    def test_opened_polls_if_exists_these_polls(self):

        Poll.objects.filter().delete()

        PollFactory(status='draft')
        poll1 = PollFactory(status='opened')
        poll2 = PollFactory(status='opened')
        PollFactory(status='closed')

        self.assertCountEqual(Poll.objects.opened_polls(), (poll1, poll2))

    def test_closed_polls_if_exists_these_polls(self):

        Poll.objects.filter().delete()

        PollFactory(status='draft')
        poll1 = PollFactory(status='closed')
        poll2 = PollFactory(status='closed')
        PollFactory(status='opened')

        self.assertCountEqual(Poll.objects.closed_polls(), (poll1, poll2))

    def test_draft_polls_if_exists_these_polls(self):

        Poll.objects.filter().delete()

        PollFactory(status='opened')
        poll1 = PollFactory(status='draft')
        poll2 = PollFactory(status='draft')
        PollFactory(status='closed')

        self.assertCountEqual(Poll.objects.draft_polls(), (poll1, poll2))

    def test_polls_with_count_votes_if_exists_not_votes(self):

        # get a queryset
        polls_with_count_votes = Poll.objects.polls_with_count_votes()

        # get values of fields
        values_polls_with_count_votes = polls_with_count_votes.values('pk', 'count_votes')

        self.assertCountEqual(
            values_polls_with_count_votes,
            (
                {'pk': self.poll1.pk, 'count_votes': 0},
                {'pk': self.poll2.pk, 'count_votes': 0},
                {'pk': self.poll3.pk, 'count_votes': 0},
                {'pk': self.poll4.pk, 'count_votes': 0},
                {'pk': self.poll5.pk, 'count_votes': 0},
                {'pk': self.poll6.pk, 'count_votes': 0},
                {'pk': self.poll7.pk, 'count_votes': 0},
                {'pk': self.poll8.pk, 'count_votes': 0},
                {'pk': self.poll9.pk, 'count_votes': 0},
            )
        )

    def test_polls_with_count_votes_if_exists_votes(self):

        # add votes
        # iteration contains a record as (poll, unique users)
        for poll, users in (
            (self.poll1, User.objects.random_users(4)),
            (self.poll3, User.objects.random_users(6)),
            (self.poll4, User.objects.random_users(30)),
            (self.poll5, User.objects.random_users(29)),
            (self.poll6, User.objects.random_users(15)),
            (self.poll7, User.objects.random_users(5)),
            (self.poll8, User.objects.random_users(10)),
            (self.poll9, [User.objects.random_users(1)]),
        ):

            # add votes to a list, in order to create the votes with a one query
            query = list()
            for user in users:
                query.append(Vote(poll=poll, user=user, choice=random.choice(poll.choices.all())))
            Vote.objects.bulk_create(query)

        # get a queryset
        polls_with_count_votes = Poll.objects.polls_with_count_votes()

        # get values of fields
        values_polls_with_count_votes = polls_with_count_votes.values('pk', 'count_votes')

        self.assertCountEqual(
            values_polls_with_count_votes,
            (
                {'pk': self.poll1.pk, 'count_votes': 4},
                {'pk': self.poll2.pk, 'count_votes': 0},
                {'pk': self.poll3.pk, 'count_votes': 6},
                {'pk': self.poll4.pk, 'count_votes': 30},
                {'pk': self.poll5.pk, 'count_votes': 29},
                {'pk': self.poll6.pk, 'count_votes': 15},
                {'pk': self.poll7.pk, 'count_votes': 5},
                {'pk': self.poll8.pk, 'count_votes': 10},
                {'pk': self.poll9.pk, 'count_votes': 1},
            )
        )

    def test_polls_with_count_choices_if_exists_not_choices(self):

        # delete all choices
        Choice.objects.filter().delete()

        # get a queryset
        polls_with_count_choices = Poll.objects.polls_with_count_choices()

        # get values of fields
        values_polls_with_count_choices = polls_with_count_choices.values('pk', 'count_choices')

        self.assertCountEqual(
            values_polls_with_count_choices,
            (
                {'pk': self.poll1.pk, 'count_choices': 0},
                {'pk': self.poll2.pk, 'count_choices': 0},
                {'pk': self.poll3.pk, 'count_choices': 0},
                {'pk': self.poll4.pk, 'count_choices': 0},
                {'pk': self.poll5.pk, 'count_choices': 0},
                {'pk': self.poll6.pk, 'count_choices': 0},
                {'pk': self.poll7.pk, 'count_choices': 0},
                {'pk': self.poll8.pk, 'count_choices': 0},
                {'pk': self.poll9.pk, 'count_choices': 0},
            )
        )

    def test_polls_with_count_choices_if_exists_choices(self):

        # get a queryset
        polls_with_count_choices = Poll.objects.polls_with_count_choices()

        # get values of fields
        values_polls_with_count_choices = polls_with_count_choices.values('pk', 'count_choices')

        self.assertCountEqual(
            values_polls_with_count_choices,
            (
                {'pk': self.poll1.pk, 'count_choices': 8},
                {'pk': self.poll2.pk, 'count_choices': 2},
                {'pk': self.poll3.pk, 'count_choices': 3},
                {'pk': self.poll4.pk, 'count_choices': 4},
                {'pk': self.poll5.pk, 'count_choices': 4},
                {'pk': self.poll6.pk, 'count_choices': 2},
                {'pk': self.poll7.pk, 'count_choices': 3},
                {'pk': self.poll8.pk, 'count_choices': 5},
                {'pk': self.poll9.pk, 'count_choices': 7},
            )
        )

    def polls_with_date_lastest_voting_if_exists_not_votes(self):

        # get a queryset
        polls_with_date_lastest_voting = Poll.objects.polls_with_date_lastest_voting()

        # get values of fields
        values_polls_with_date_lastest_voting = polls_with_date_lastest_voting.values('pk', 'date_lastest_voting')

        self.assertCountEqual(
            values_polls_with_date_lastest_voting,
            (
                {'pk': self.poll1.pk, 'date_lastest_voting': None},
                {'pk': self.poll2.pk, 'date_lastest_voting': None},
                {'pk': self.poll3.pk, 'date_lastest_voting': None},
                {'pk': self.poll4.pk, 'date_lastest_voting': None},
                {'pk': self.poll5.pk, 'date_lastest_voting': None},
                {'pk': self.poll6.pk, 'date_lastest_voting': None},
                {'pk': self.poll7.pk, 'date_lastest_voting': None},
                {'pk': self.poll8.pk, 'date_lastest_voting': None},
                {'pk': self.poll9.pk, 'date_lastest_voting': None},
            )
        )

    def polls_with_date_lastest_voting_if_votes_exists(self):

        # add votes

        # 1
        self.poll1.votes.create(user=self.user1, choice=self.poll1.choices.last())
        self.poll1.votes.create(user=self.user2, choice=self.poll1.choices.last())
        latest_vote_poll1 = self.poll1.votes.create(user=self.user3, choice=self.poll1.choices.first())

        # 2
        latest_vote_poll2 = self.poll2.votes.create(user=self.user4, choice=self.poll2.choices.last())

        # 3
        self.poll3.votes.create(user=self.user5, choice=self.poll3.choices.last())
        latest_vote_poll3 = self.poll3.votes.create(user=self.user1, choice=self.poll3.choices.last())

        # 4
        self.poll4.votes.create(user=self.user2, choice=self.poll4.choices.first())
        self.poll4.votes.create(user=self.user3, choice=self.poll4.choices.last())
        self.poll4.votes.create(user=self.user4, choice=self.poll4.choices.last())
        latest_vote_poll4 = self.poll4.votes.create(user=self.user5, choice=self.poll4.choices.first())

        # 5
        latest_vote_poll5 = self.poll5.votes.create(user=self.user1, choice=self.poll5.choices.last())

        # 6
        self.poll6.votes.create(user=self.user2, choice=self.poll6.choices.last())
        latest_vote_poll6 = self.poll6.votes.create(user=self.user3, choice=self.poll6.choices.first())

        # 7
        latest_vote_poll7 = self.poll7.votes.create(user=self.user4, choice=self.poll7.choices.last())

        # get a queryset
        polls_with_date_lastest_voting = Poll.objects.polls_with_date_lastest_voting()

        # get values of fields
        values_polls_with_date_lastest_voting = polls_with_date_lastest_voting.values('pk', 'date_lastest_voting')

        self.assertCountEqual(
            values_polls_with_date_lastest_voting,
            (
                {'pk': self.poll1.pk, 'date_lastest_voting': latest_vote_poll1.date_voting},
                {'pk': self.poll2.pk, 'date_lastest_voting': latest_vote_poll2.date_voting},
                {'pk': self.poll3.pk, 'date_lastest_voting': latest_vote_poll3.date_voting},
                {'pk': self.poll4.pk, 'date_lastest_voting': latest_vote_poll4.date_voting},
                {'pk': self.poll5.pk, 'date_lastest_voting': latest_vote_poll5.date_voting},
                {'pk': self.poll6.pk, 'date_lastest_voting': latest_vote_poll6.date_voting},
                {'pk': self.poll7.pk, 'date_lastest_voting': latest_vote_poll7.date_voting},
                {'pk': self.poll8.pk, 'date_lastest_voting': None},
                {'pk': self.poll9.pk, 'date_lastest_voting': None},

            )
        )

    def test_polls_with_count_choices_and_votes_and_date_lastest_voting_if_exists_not_all_needed(self):

        # delete all choices
        Choice.objects.filter().delete()

        # annonate a queryset
        polls_with_count_choices_and_votes_and_date_lastest_voting = \
            Poll.objects.polls_with_count_choices_and_votes_and_date_lastest_voting()

        # get values of fields
        values_polls_with_count_choices_and_votes_and_date_lastest_voting = \
            polls_with_count_choices_and_votes_and_date_lastest_voting.values(
                'pk', 'count_choices', 'count_votes', 'date_latest_voting'
            )

        self.assertCountEqual(
            values_polls_with_count_choices_and_votes_and_date_lastest_voting,
            (
                {'pk': self.poll1.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll2.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll3.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll4.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll5.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll6.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll7.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll8.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
                {'pk': self.poll9.pk, 'count_votes': 0, 'count_choices': 0, 'date_latest_voting': None},
            )
        )

    def test_polls_with_count_choices_and_votes_and_date_lastest_voting_if_all_needed_exists(self):

        # add votes

        # 1
        self.poll1.votes.create(user=self.user1, choice=self.poll1.choices.last())
        self.poll1.votes.create(user=self.user2, choice=self.poll1.choices.last())
        self.poll1.votes.create(user=self.user3, choice=self.poll1.choices.last())
        self.poll1.votes.create(user=self.user4, choice=self.poll1.choices.last())
        lst_vote1 = self.poll1.votes.create(user=self.user5, choice=self.poll1.choices.first())
        date_lst_vote1 = lst_vote1.date_voting

        # 2
        lst_vote2 = self.poll2.votes.create(user=self.user4, choice=self.poll2.choices.last())
        date_lst_vote2 = lst_vote2.date_voting

        # 3
        self.poll3.votes.create(user=self.user5, choice=self.poll3.choices.last())
        lst_vote3 = self.poll3.votes.create(user=self.user1, choice=self.poll3.choices.last())
        date_lst_vote3 = lst_vote3.date_voting

        # 4
        self.poll4.votes.create(user=self.user1, choice=self.poll4.choices.first())
        self.poll4.votes.create(user=self.user2, choice=self.poll4.choices.last())
        self.poll4.votes.create(user=self.user3, choice=self.poll4.choices.last())
        self.poll4.votes.create(user=self.user4, choice=self.poll4.choices.last())
        lst_vote4 = self.poll4.votes.create(user=self.user5, choice=self.poll4.choices.first())
        date_lst_vote4 = lst_vote4.date_voting

        # 5
        lst_vote5 = self.poll5.votes.create(user=self.user1, choice=self.poll5.choices.last())
        date_lst_vote5 = lst_vote5.date_voting

        # 6
        self.poll6.votes.create(user=self.user1, choice=self.poll6.choices.last())
        self.poll6.votes.create(user=self.user2, choice=self.poll6.choices.last())
        self.poll6.votes.create(user=self.user3, choice=self.poll6.choices.last())
        self.poll6.votes.create(user=self.user4, choice=self.poll6.choices.last())
        lst_vote6 = self.poll6.votes.create(user=self.user5, choice=self.poll6.choices.first())
        date_lst_vote6 = lst_vote6.date_voting

        # 7
        lst_vote7 = self.poll7.votes.create(user=self.user4, choice=self.poll7.choices.last())
        date_lst_vote7 = lst_vote7.date_voting

        # annonate a queryset
        polls_with_count_choices_and_votes_and_date_lastest_voting = \
            Poll.objects.polls_with_count_choices_and_votes_and_date_lastest_voting()

        # get values of fields
        values_polls_with_count_choices_and_votes_and_date_lastest_voting = \
            polls_with_count_choices_and_votes_and_date_lastest_voting.values(
                'pk', 'count_choices', 'count_votes', 'date_latest_voting'
            )

        self.assertCountEqual(
            values_polls_with_count_choices_and_votes_and_date_lastest_voting,
            (
                {'pk': self.poll1.pk, 'count_votes': 5, 'count_choices': 8, 'date_latest_voting': date_lst_vote1},
                {'pk': self.poll2.pk, 'count_votes': 1, 'count_choices': 2, 'date_latest_voting': date_lst_vote2},
                {'pk': self.poll3.pk, 'count_votes': 2, 'count_choices': 3, 'date_latest_voting': date_lst_vote3},
                {'pk': self.poll4.pk, 'count_votes': 5, 'count_choices': 4, 'date_latest_voting': date_lst_vote4},
                {'pk': self.poll5.pk, 'count_votes': 1, 'count_choices': 4, 'date_latest_voting': date_lst_vote5},
                {'pk': self.poll6.pk, 'count_votes': 5, 'count_choices': 2, 'date_latest_voting': date_lst_vote6},
                {'pk': self.poll7.pk, 'count_votes': 1, 'count_choices': 3, 'date_latest_voting': date_lst_vote7},
                {'pk': self.poll8.pk, 'count_votes': 0, 'count_choices': 5, 'date_latest_voting': None},
                {'pk': self.poll9.pk, 'count_votes': 0, 'count_choices': 7, 'date_latest_voting': None},
            )
        )


class ChoiceQuerySetTest(TestCase):
    """
    Tests for queryset of choices
    """

    @classmethod
    def setUpTestData(self):

        # create users
        call_command('factory_test_users', '30')

        # create polls
        poll1 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        poll2 = PollFactory(status=Poll.CHOICES_STATUS.draft)
        poll3 = PollFactory(status=Poll.CHOICES_STATUS.closed)

        # create choices for polls
        self.choice11 = ChoiceFactory(poll=poll1)
        self.choice12 = ChoiceFactory(poll=poll1)
        self.choice13 = ChoiceFactory(poll=poll1)
        self.choice21 = ChoiceFactory(poll=poll2)
        self.choice22 = ChoiceFactory(poll=poll2)
        self.choice31 = ChoiceFactory(poll=poll3)
        self.choice32 = ChoiceFactory(poll=poll3)
        self.choice33 = ChoiceFactory(poll=poll3)
        self.choice34 = ChoiceFactory(poll=poll3)

        #
        users = User.objects.random_users(10)
        for user in users[0:3]:
            Vote.objects.create(poll=self.choice11.poll, user=user, choice=self.choice11)
        for user in users[3:6]:
            Vote.objects.create(poll=self.choice12.poll, user=user, choice=self.choice12)
        for user in users[6:11]:
            Vote.objects.create(poll=self.choice13.poll, user=user, choice=self.choice13)
        #
        users = User.objects.random_users(20)
        for user in users[0:4]:
            Vote.objects.create(poll=self.choice21.poll, user=user, choice=self.choice21)
        for user in users[4:21]:
            Vote.objects.create(poll=self.choice22.poll, user=user, choice=self.choice22)
        #
        users = User.objects.random_users(30)
        Vote.objects.create(poll=self.choice31.poll, user=users[0], choice=self.choice31)

        for user in users[1:20]:
            Vote.objects.create(poll=self.choice33.poll, user=user, choice=self.choice33)

        for user in users[20:31]:
            Vote.objects.create(poll=self.choice34.poll, user=user, choice=self.choice34)

    def test_choices_with_count_votes(self):

        # annotate a queryset
        choices_with_count_votes = Choice.objects.choices_with_count_votes()

        # get values of fields
        values_choices_with_count_votes = choices_with_count_votes.values('pk', 'count_votes')

        self.assertCountEqual(
            values_choices_with_count_votes,
            (
                {'pk': self.choice11.pk, 'count_votes': 3},
                {'pk': self.choice12.pk, 'count_votes': 3},
                {'pk': self.choice13.pk, 'count_votes': 4},
                {'pk': self.choice21.pk, 'count_votes': 4},
                {'pk': self.choice22.pk, 'count_votes': 16},
                {'pk': self.choice31.pk, 'count_votes': 1},
                {'pk': self.choice32.pk, 'count_votes': 0},
                {'pk': self.choice33.pk, 'count_votes': 19},
                {'pk': self.choice34.pk, 'count_votes': 10},
            )
        )


class UserPollQuerySetTest(TestCase):
    """
    Tests for a QuerySet, attached to the User model, throught a corresponding manager or as alone.
    """

    @classmethod
    def setUpTestData(cls):

        # create users
        call_command('factory_test_users', '5')

        cls.user1, cls.user2, cls.user3, cls.user4, cls.user5 = User.objects.all()

    def setUp(self):

        # create polls with choices
        call_command('factory_test_polls', '5', '--without-votes')

        self.poll1, self.poll2, self.poll3, self.poll4, self.poll5 = Poll.objects.all()

    def test_users_with_count_votes_if_exists_no_votes(self):

        # annotate a queryset
        users_with_count_votes = User.polls.users_with_count_votes()

        # values of fields
        values_users_with_count_votes = users_with_count_votes.values('pk', 'count_votes')

        self.assertCountEqual(
            values_users_with_count_votes,
            (
                {'pk': self.user1.pk, 'count_votes': 0},
                {'pk': self.user2.pk, 'count_votes': 0},
                {'pk': self.user3.pk, 'count_votes': 0},
                {'pk': self.user4.pk, 'count_votes': 0},
                {'pk': self.user5.pk, 'count_votes': 0},
            )
        )

    def test_users_with_count_votes_if_exists_votes(self):

        # add votes
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user3.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user5.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        # annotate a queryset
        users_with_count_votes = User.polls.users_with_count_votes()

        # values of fields
        values_users_with_count_votes = users_with_count_votes.values('pk', 'count_votes')

        self.assertCountEqual(
            values_users_with_count_votes,
            (
                {'pk': self.user1.pk, 'count_votes': 4},
                {'pk': self.user2.pk, 'count_votes': 0},
                {'pk': self.user3.pk, 'count_votes': 2},
                {'pk': self.user4.pk, 'count_votes': 1},
                {'pk': self.user5.pk, 'count_votes': 3},
            )
        )

    def test_users_with_date_latest_voting_if_exists_no_votes(self):

        # annotate a queryset
        users_with_date_latest_voting = User.polls.users_with_date_latest_voting()

        # values of fields
        values_users_with_date_latest_voting = users_with_date_latest_voting.values('pk', 'date_latest_voting')

        self.assertCountEqual(
            values_users_with_date_latest_voting,
            (
                {'pk': self.user1.pk, 'date_latest_voting': None},
                {'pk': self.user2.pk, 'date_latest_voting': None},
                {'pk': self.user3.pk, 'date_latest_voting': None},
                {'pk': self.user4.pk, 'date_latest_voting': None},
                {'pk': self.user5.pk, 'date_latest_voting': None},
            )
        )

    def test_users_with_date_latest_voting_if_exists_votes(self):

        # add votes

        # 1
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        lst_vote1 = self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        date_lst_vote1 = lst_vote1.date_voting

        # 3
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        lst_vote3 = self.user3.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        date_lst_vote3 = lst_vote3.date_voting

        # 4
        lst_vote4 = self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        date_lst_vote4 = lst_vote4.date_voting

        # 5
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        lst_vote5 = self.user5.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        date_lst_vote5 = lst_vote5.date_voting

        # annotate a queryset
        users_with_date_latest_voting = User.polls.users_with_date_latest_voting()

        # values of fields
        values_users_with_date_latest_voting = users_with_date_latest_voting.values('pk', 'date_latest_voting')

        self.assertCountEqual(
            values_users_with_date_latest_voting,
            (
                {'pk': self.user1.pk, 'date_latest_voting': date_lst_vote1},
                {'pk': self.user2.pk, 'date_latest_voting': None},
                {'pk': self.user3.pk, 'date_latest_voting': date_lst_vote3},
                {'pk': self.user4.pk, 'date_latest_voting': date_lst_vote4},
                {'pk': self.user5.pk, 'date_latest_voting': date_lst_vote5},
            )
        )

    def test_users_with_active_voters_status_if_exists_not_polls(self):

        # delete all polls
        Poll.objects.filter().delete()

        # annotate a queryset
        users_with_active_voters_status = User.polls.users_with_active_voters_status()

        # values of fields
        values_users_with_active_voters_status = users_with_active_voters_status.values('pk', 'is_active_voter')

        self.assertCountEqual(
            values_users_with_active_voters_status,
            (
                {'pk': self.user1.pk, 'is_active_voter': False},
                {'pk': self.user2.pk, 'is_active_voter': False},
                {'pk': self.user3.pk, 'is_active_voter': False},
                {'pk': self.user4.pk, 'is_active_voter': False},
                {'pk': self.user5.pk, 'is_active_voter': False},
            )
        )

    def test_users_with_active_voters_status_if_exist_polls_but_exists_not_votes(self):

        # test with 5 polls
        self.assertEqual(Poll.objects.count(), 5)

        # annotate a queryset
        users_with_active_voters_status = User.polls.users_with_active_voters_status()

        values_users_with_active_voters_status = users_with_active_voters_status.values('pk', 'is_active_voter')

        self.assertCountEqual(
            values_users_with_active_voters_status,
            (
                {'pk': self.user1.pk, 'is_active_voter': False},
                {'pk': self.user2.pk, 'is_active_voter': False},
                {'pk': self.user3.pk, 'is_active_voter': False},
                {'pk': self.user4.pk, 'is_active_voter': False},
                {'pk': self.user5.pk, 'is_active_voter': False},
            )
        )

    def test_users_with_active_voters_status_if_exist_1_poll_and_exists_votes(self):

        # test with 1 poll
        self.poll2.delete()
        self.poll3.delete()
        self.poll4.delete()
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 1)

        # Add Votes
        #
        # the user1 has 1 vote
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user2 has no votes
        # the user3 has no votes
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user4 has 1 vote
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user5 has no votes

        # annotate a queryset
        users_with_active_voters_status = User.polls.users_with_active_voters_status()

        values_users_with_active_voters_status = users_with_active_voters_status.values('pk', 'is_active_voter')

        self.assertCountEqual(
            values_users_with_active_voters_status,
            (
                {'pk': self.user1.pk, 'is_active_voter': True},
                {'pk': self.user2.pk, 'is_active_voter': False},
                {'pk': self.user3.pk, 'is_active_voter': True},
                {'pk': self.user4.pk, 'is_active_voter': True},
                {'pk': self.user5.pk, 'is_active_voter': False},
            )
        )

    def test_users_with_active_voters_status_if_exist_2_polls_and_exists_votes(self):

        # test with 2 polls
        self.poll3.delete()
        self.poll4.delete()
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 2)

        # Add Votes
        #
        # the user1 has no votes

        # the user2 has 2 vote
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # the user3 has 1 vote
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user4 has no votes
        # the user5 has no votes
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # annotate a queryset
        users_with_active_voters_status = User.polls.users_with_active_voters_status()

        values_users_with_active_voters_status = users_with_active_voters_status.values('pk', 'is_active_voter')

        self.assertCountEqual(
            values_users_with_active_voters_status,
            (
                {'pk': self.user1.pk, 'is_active_voter': False},
                {'pk': self.user2.pk, 'is_active_voter': True},
                {'pk': self.user3.pk, 'is_active_voter': False},
                {'pk': self.user4.pk, 'is_active_voter': False},
                {'pk': self.user5.pk, 'is_active_voter': True},
            )
        )

    def test_users_with_active_voters_status_if_exist_3_polls_and_exists_votes(self):

        # test with 3 polls
        self.poll4.delete()
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 3)

        # Add Votes
        #
        # the user1 has 1 vote
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user2 has 3 votes
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # the user3 has 2 votes
        self.user3.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # the user4 has 1 vote
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user5 has no votes

        # annotate a queryset
        users_with_active_voters_status = User.polls.users_with_active_voters_status()

        values_users_with_active_voters_status = users_with_active_voters_status.values('pk', 'is_active_voter')

        self.assertCountEqual(
            values_users_with_active_voters_status,
            (
                {'pk': self.user1.pk, 'is_active_voter': False},
                {'pk': self.user2.pk, 'is_active_voter': True},
                {'pk': self.user3.pk, 'is_active_voter': True},
                {'pk': self.user4.pk, 'is_active_voter': False},
                {'pk': self.user5.pk, 'is_active_voter': False},
            )
        )

    def test_users_with_active_voters_status_if_exist_4_polls_and_exists_votes(self):

        # test with 4 polls
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 4)

        # Add Votes
        #
        # the user1 has 4 votes
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())

        # the user2 has 2 votes
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # the user3 has no votes

        # the user4 has 1 vote
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user5 has 3 votes
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user5.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # annotate a queryset
        users_with_active_voters_status = User.polls.users_with_active_voters_status()

        values_users_with_active_voters_status = users_with_active_voters_status.values('pk', 'is_active_voter')

        self.assertCountEqual(
            values_users_with_active_voters_status,
            (
                {'pk': self.user1.pk, 'is_active_voter': True},
                {'pk': self.user2.pk, 'is_active_voter': False},
                {'pk': self.user3.pk, 'is_active_voter': False},
                {'pk': self.user4.pk, 'is_active_voter': False},
                {'pk': self.user5.pk, 'is_active_voter': True},
            )
        )

    def test_users_with_active_voters_status_if_exist_5_polls_and_exists_votes(self):

        # test with 5 polls
        self.assertEqual(Poll.objects.count(), 5)

        # Add Votes
        #
        # the user1 has 4 votes
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())

        # the user2 has 2 votes
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # the user3 has no votes

        # the user4 has 3 votes
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user4.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user4.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # the user5 has 5 vote
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user5.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user5.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user5.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        # annotate a queryset
        users_with_active_voters_status = User.polls.users_with_active_voters_status()

        values_users_with_active_voters_status = users_with_active_voters_status.values('pk', 'is_active_voter')

        self.assertCountEqual(
            values_users_with_active_voters_status,
            (
                {'pk': self.user1.pk, 'is_active_voter': True},
                {'pk': self.user2.pk, 'is_active_voter': False},
                {'pk': self.user3.pk, 'is_active_voter': False},
                {'pk': self.user4.pk, 'is_active_voter': True},
                {'pk': self.user5.pk, 'is_active_voter': True},
            )
        )

    def test_users_as_voters_if_exists_not_polls(self):

        # delete all polls
        Poll.objects.filter().delete()

        # annotate a queryset
        users_as_voters = User.polls.users_as_voters()

        # values of fields
        values_users_as_voters = users_as_voters.values('pk', 'is_active_voter', 'count_votes')

        self.assertCountEqual(
            values_users_as_voters,
            (
                {'pk': self.user1.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user2.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user3.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user4.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user5.pk, 'is_active_voter': False, 'count_votes': 0},
            )
        )

    def test_users_as_voters_if_exist_polls_but_exists_not_votes(self):

        # test with 5 polls
        self.assertEqual(Poll.objects.count(), 5)

        # annotate a queryset
        users_as_voters = User.polls.users_as_voters()

        values_users_as_voters = users_as_voters.values('pk', 'is_active_voter', 'count_votes')

        self.assertCountEqual(
            values_users_as_voters,
            (
                {'pk': self.user1.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user2.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user3.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user4.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user5.pk, 'is_active_voter': False, 'count_votes': 0},
            )
        )

    def test_users_as_voters_if_exist_1_poll_and_exists_votes(self):

        # test with 1 poll
        self.poll2.delete()
        self.poll3.delete()
        self.poll4.delete()
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 1)

        # Add Votes
        #
        # the user1 has 1 vote
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user2 has no votes
        # the user3 has no votes
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user4 has 1 vote
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user5 has no votes

        # annotate a queryset
        users_as_voters = User.polls.users_as_voters()

        values_users_as_voters = users_as_voters.values('pk', 'is_active_voter', 'count_votes')

        self.assertCountEqual(
            values_users_as_voters,
            (
                {'pk': self.user1.pk, 'is_active_voter': True, 'count_votes': 1},
                {'pk': self.user2.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user3.pk, 'is_active_voter': True, 'count_votes': 1},
                {'pk': self.user4.pk, 'is_active_voter': True, 'count_votes': 1},
                {'pk': self.user5.pk, 'is_active_voter': False, 'count_votes': 0},
            )
        )

    def test_users_as_voters_if_exist_2_polls_and_exists_votes(self):

        # test with 2 polls
        self.poll3.delete()
        self.poll4.delete()
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 2)

        # Add Votes
        #
        # the user1 has no votes

        # the user2 has 2 vote
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # the user3 has 1 vote
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user4 has no votes

        # the user5 has 2 votes
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # annotate a queryset
        users_as_voters = User.polls.users_as_voters()

        values_users_as_voters = users_as_voters.values('pk', 'is_active_voter', 'count_votes')

        self.assertCountEqual(
            values_users_as_voters,
            (
                {'pk': self.user1.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user2.pk, 'is_active_voter': True, 'count_votes': 2},
                {'pk': self.user3.pk, 'is_active_voter': False, 'count_votes': 1},
                {'pk': self.user4.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user5.pk, 'is_active_voter': True, 'count_votes': 2},
            )
        )

    def test_users_as_voters_if_exist_3_polls_and_exists_votes(self):

        # test with 3 polls
        self.poll4.delete()
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 3)

        # Add Votes
        #
        # the user1 has 1 vote
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user2 has 3 votes
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # the user3 has 2 votes
        self.user3.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # the user4 has 1 vote
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user5 has no votes

        # annotate a queryset
        users_as_voters = User.polls.users_as_voters()

        values_users_as_voters = users_as_voters.values('pk', 'is_active_voter', 'count_votes')

        self.assertCountEqual(
            values_users_as_voters,
            (
                {'pk': self.user1.pk, 'is_active_voter': False, 'count_votes': 1},
                {'pk': self.user2.pk, 'is_active_voter': True, 'count_votes': 3},
                {'pk': self.user3.pk, 'is_active_voter': True, 'count_votes': 2},
                {'pk': self.user4.pk, 'is_active_voter': False, 'count_votes': 1},
                {'pk': self.user5.pk, 'is_active_voter': False, 'count_votes': 0},
            )
        )

    def test_users_as_voters_if_exist_4_polls_and_exists_votes(self):

        # test with 4 polls
        self.poll5.delete()
        self.assertEqual(Poll.objects.count(), 4)

        # Add Votes
        #
        # the user1 has 4 votes
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())

        # the user2 has 2 votes
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # the user3 has no votes

        # the user4 has 1 vote
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        # the user5 has 3 votes
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user5.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # annotate a queryset
        users_as_voters = User.polls.users_as_voters()

        values_users_as_voters = users_as_voters.values('pk', 'is_active_voter', 'count_votes')

        self.assertCountEqual(
            values_users_as_voters,
            (
                {'pk': self.user1.pk, 'is_active_voter': True, 'count_votes': 4},
                {'pk': self.user2.pk, 'is_active_voter': False, 'count_votes': 2},
                {'pk': self.user3.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user4.pk, 'is_active_voter': False, 'count_votes': 1},
                {'pk': self.user5.pk, 'is_active_voter': True, 'count_votes': 3},
            )
        )

    def test_users_as_voters_if_exist_5_polls_and_exists_votes(self):

        # test with 5 polls
        self.assertEqual(Poll.objects.count(), 5)

        # Add Votes
        #
        # the user1 has 4 votes
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())

        # the user2 has 2 votes
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        # the user3 has no votes

        # the user4 has 3 votes
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user4.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user4.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        # the user5 has 5 vote
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user5.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user5.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user5.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        # annotate a queryset
        users_as_voters = User.polls.users_as_voters()

        values_users_as_voters = users_as_voters.values('pk', 'is_active_voter', 'count_votes')

        self.assertCountEqual(
            values_users_as_voters,
            (
                {'pk': self.user1.pk, 'is_active_voter': True, 'count_votes': 4},
                {'pk': self.user2.pk, 'is_active_voter': False, 'count_votes': 2},
                {'pk': self.user3.pk, 'is_active_voter': False, 'count_votes': 0},
                {'pk': self.user4.pk, 'is_active_voter': True, 'count_votes': 3},
                {'pk': self.user5.pk, 'is_active_voter': True, 'count_votes': 5},
            )
        )
