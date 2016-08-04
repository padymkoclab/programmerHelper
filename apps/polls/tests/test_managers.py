
import random

from django.test import TestCase

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll, Vote
from apps.users.factories import UserFactory
from apps.users.models import User


class PollManagerTest(TestCase):
    """
    Tests for manager of polls.
    """

    def _generate_polls_choices_votes(self):
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

        # iteration as poll, count votes by unique users
        for poll, users in (
            (self.poll1, User.objects.active_users().random_users(4)),
            (self.poll3, User.objects.active_users().random_users(6)),
            (self.poll4, User.objects.active_users().random_users(30)),
            (self.poll5, User.objects.active_users().random_users(29)),
            (self.poll6, User.objects.active_users().random_users(31)),
            (self.poll7, User.objects.active_users().random_users(5)),
            (self.poll8, User.objects.active_users().random_users(10)),
            (self.poll9, [User.objects.active_users().random_users(1)]),
        ):
            for user in users:
                vote = Vote(poll=poll, user=user, choice=random.choice(poll.choices.all()))
                vote.full_clean()
                vote.save()

    @classmethod
    def setUpTestData(cls):

        # create users
        for i in range(40):
            UserFactory(is_active=True)

        #
        cls._generate_polls_choices_votes(cls)

    def test_most_activity_voters_if_queryset_is_empty(self):
        Poll.objects.filter().delete()
        self.assertEqual(Poll.objects.count(), 0)
        self.assertQuerysetEqual(Poll.objects.most_activity_voters(), ())

        # restore initialization polls, choices and votes
        self._generate_polls_choices_votes()

    def test_most_activity_voters_if_queryset_have_single_poll(self):
        Poll.objects.exclude(pk=self.poll1.pk).delete()
        self.assertEqual(Poll.objects.count(), 1)
        #
        self.assertCountEqual(
            Poll.objects.most_activity_voters(),
            User.objects.users_with_count_votes().filter(count_votes__gt=0)
        )
        # restore initialization polls, choices and votes
        self._generate_polls_choices_votes()

    def test_most_activity_voters_if_queryset_have_two_poll(self):
        Poll.objects.exclude(pk__in=[self.poll1.pk, self.poll4.pk]).delete()
        self.assertEqual(Poll.objects.count(), 2)

        #
        self.assertCountEqual(
            Poll.objects.most_activity_voters(),
            User.objects.users_with_count_votes().filter(count_votes__gt=1)
        )

        # restore initialization polls, choices and votes
        self._generate_polls_choices_votes()

    def test_most_activity_voters_if_queryset_have_eight_poll(self):
        Poll.objects.filter(pk=self.poll5.pk).delete()
        self.assertEqual(Poll.objects.count(), 8)

        #
        self.assertCountEqual(
            Poll.objects.most_activity_voters(),
            User.objects.users_with_count_votes().filter(count_votes__gt=4)
        )

        # restore initialization polls, choices and votes
        self._generate_polls_choices_votes()

    def test_most_activity_voters_if_queryset_have_nine_poll(self):
        self.assertEqual(Poll.objects.count(), 9)

        #
        self.assertCountEqual(
            Poll.objects.most_activity_voters(),
            User.objects.users_with_count_votes().filter(count_votes__gt=4)
        )

        # restore initialization polls, choices and votes
        self._generate_polls_choices_votes()

    def test_get_all_voters(self):
        self.assertCountEqual(
            Poll.objects.get_all_voters(),
            User.objects.users_with_count_votes().filter(count_votes__gt=0),
        )
