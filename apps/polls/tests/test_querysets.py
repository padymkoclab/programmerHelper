
import random

from django.test import TestCase

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll, Choice, Vote
from apps.users.factories import UserFactory
from apps.users.models import User


class PollQuerySetTest(TestCase):
    """
    Tests for queryset of polls.
    """

    @classmethod
    def setUpTestData(cls):

        # create users
        for i in range(35):
            UserFactory(is_active=True)

        # create polls
        cls.poll1 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        cls.poll2 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        cls.poll3 = PollFactory(status=Poll.CHOICES_STATUS.draft)
        cls.poll4 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        cls.poll5 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        cls.poll6 = PollFactory(status=Poll.CHOICES_STATUS.draft)
        cls.poll7 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        cls.poll8 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        cls.poll9 = PollFactory(status=Poll.CHOICES_STATUS.closed)

        # create choices for polls
        for poll, count_choices in (
            (cls.poll1, 8),
            (cls.poll2, 2),
            (cls.poll3, 3),
            (cls.poll4, 4),
            (cls.poll5, 4),
            (cls.poll6, 2),
            (cls.poll7, 3),
            (cls.poll8, 5),
            (cls.poll9, 7),
        ):
            for i in range(count_choices):
                ChoiceFactory(poll=poll)

        # iteration as poll, count votes by unique users
        for poll, users in (
            (cls.poll1, User.objects.active_users().random_users(4)),
            (cls.poll3, User.objects.active_users().random_users(6)),
            (cls.poll4, User.objects.active_users().random_users(30)),
            (cls.poll5, User.objects.active_users().random_users(29)),
            (cls.poll6, User.objects.active_users().random_users(31)),
            (cls.poll7, User.objects.active_users().random_users(5)),
            (cls.poll8, User.objects.active_users().random_users(10)),
            (cls.poll9, [User.objects.active_users().random_users(1)]),
        ):
            for user in users:
                vote = Vote(poll=poll, user=user, choice=random.choice(poll.choices.all()))
                vote.full_clean()
                vote.save()

    def test_closed_polls(self):
        self.assertCountEqual(
            Poll.objects.closed_polls(),
            [self.poll1, self.poll5, self.poll8, self.poll9]
        )

    def test_opened_polls(self):
        self.assertCountEqual(
            Poll.objects.opened_polls(),
            [self.poll2, self.poll4, self.poll7]
        )

    def test_draft_polls(self):
        self.assertCountEqual(Poll.objects.draft_polls(), [self.poll3, self.poll6])

    def test_polls_with_count_votes(self):
        polls_with_count_votes = Poll.objects.polls_with_count_votes()
        self.assertEqual(polls_with_count_votes.get(pk=self.poll1.pk).count_votes, 4)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll2.pk).count_votes, 0)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll3.pk).count_votes, 6)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll4.pk).count_votes, 30)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll5.pk).count_votes, 29)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll6.pk).count_votes, 31)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll7.pk).count_votes, 5)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll8.pk).count_votes, 10)
        self.assertEqual(polls_with_count_votes.get(pk=self.poll9.pk).count_votes, 1)

    def test_polls_with_high_activity(self):
        self.assertCountEqual(
            Poll.objects.polls_with_high_activity(),
            (self.poll4, self.poll6),
        )

    def test_polls_with_low_activity(self):
        self.assertCountEqual(
            Poll.objects.polls_with_low_activity(),
            (self.poll1, self.poll2, self.poll9),
        )

    def test_polls_with_count_choices(self):
        polls_with_count_choices = Poll.objects.polls_with_count_choices()
        self.assertEqual(polls_with_count_choices.get(pk=self.poll1.pk).count_choices, 8)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll2.pk).count_choices, 2)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll3.pk).count_choices, 3)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll4.pk).count_choices, 4)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll5.pk).count_choices, 4)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll6.pk).count_choices, 2)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll7.pk).count_choices, 3)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll8.pk).count_choices, 5)
        self.assertEqual(polls_with_count_choices.get(pk=self.poll9.pk).count_choices, 7)

    def test_polls_with_count_choices_and_votes(self):
        polls_with_count_choices_and_votes = Poll.objects.polls_with_count_choices_and_votes()
        poll1 = polls_with_count_choices_and_votes.get(pk=self.poll1.pk)
        poll2 = polls_with_count_choices_and_votes.get(pk=self.poll2.pk)
        poll3 = polls_with_count_choices_and_votes.get(pk=self.poll3.pk)
        poll4 = polls_with_count_choices_and_votes.get(pk=self.poll4.pk)
        poll5 = polls_with_count_choices_and_votes.get(pk=self.poll5.pk)
        poll6 = polls_with_count_choices_and_votes.get(pk=self.poll6.pk)
        poll7 = polls_with_count_choices_and_votes.get(pk=self.poll7.pk)
        poll8 = polls_with_count_choices_and_votes.get(pk=self.poll8.pk)
        poll9 = polls_with_count_choices_and_votes.get(pk=self.poll9.pk)
        #
        self.assertEqual(poll1.count_votes, 4)
        self.assertEqual(poll2.count_votes, 0)
        self.assertEqual(poll3.count_votes, 6)
        self.assertEqual(poll4.count_votes, 30)
        self.assertEqual(poll5.count_votes, 29)
        self.assertEqual(poll6.count_votes, 31)
        self.assertEqual(poll7.count_votes, 5)
        self.assertEqual(poll8.count_votes, 10)
        self.assertEqual(poll9.count_votes, 1)
        #
        self.assertEqual(poll1.count_choices, 8)
        self.assertEqual(poll2.count_choices, 2)
        self.assertEqual(poll3.count_choices, 3)
        self.assertEqual(poll4.count_choices, 4)
        self.assertEqual(poll5.count_choices, 4)
        self.assertEqual(poll6.count_choices, 2)
        self.assertEqual(poll7.count_choices, 3)
        self.assertEqual(poll8.count_choices, 5)
        self.assertEqual(poll9.count_choices, 7)


class ChoiceQuerySetTest(TestCase):
    """
    Tests for queryset of choices
    """

    @classmethod
    def setUpTestData(self):

        for i in range(40):
            UserFactory(is_active=True)

        # create polls
        poll1 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        poll2 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        poll3 = PollFactory(status=Poll.CHOICES_STATUS.opened)

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
        users = User.objects.active_users().random_users(10)
        for user in users[0:3]:
            vote = Vote(poll=self.choice11.poll, user=user, choice=self.choice11)
            vote.full_clean()
            vote.save()
        for user in users[3:6]:
            vote = Vote(poll=self.choice12.poll, user=user, choice=self.choice12)
            vote.full_clean()
            vote.save()
        for user in users[6:11]:
            vote = Vote(poll=self.choice13.poll, user=user, choice=self.choice13)
            vote.full_clean()
            vote.save()
        #
        users = User.objects.active_users().random_users(20)
        for user in users[0:4]:
            vote = Vote(poll=self.choice21.poll, user=user, choice=self.choice21)
            vote.full_clean()
            vote.save()
        for user in users[4:21]:
            vote = Vote(poll=self.choice22.poll, user=user, choice=self.choice22)
            vote.full_clean()
            vote.save()
        #
        users = User.objects.active_users().random_users(30)
        vote = Vote(poll=self.choice31.poll, user=users[0], choice=self.choice31)
        vote.full_clean()
        vote.save()
        for user in users[1:20]:
            vote = Vote(poll=self.choice33.poll, user=user, choice=self.choice33)
            vote.full_clean()
            vote.save()
        for user in users[20:31]:
            vote = Vote(poll=self.choice34.poll, user=user, choice=self.choice34)
            vote.full_clean()
            vote.save()

    def test_choices_with_count_votes(self):
        choices_with_count_votes = Choice.objects.choices_with_count_votes()
        self.assertEqual(choices_with_count_votes.get(pk=self.choice11.pk).count_votes, 3)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice12.pk).count_votes, 3)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice13.pk).count_votes, 4)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice21.pk).count_votes, 4)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice22.pk).count_votes, 16)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice31.pk).count_votes, 1)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice32.pk).count_votes, 0)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice33.pk).count_votes, 19)
        self.assertEqual(choices_with_count_votes.get(pk=self.choice34.pk).count_votes, 10)
