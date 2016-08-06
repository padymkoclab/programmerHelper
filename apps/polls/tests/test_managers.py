
from unittest import mock

from django.utils import timezone
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model

# import pytest
from dateutil.relativedelta import relativedelta

from apps.users.factories import UserFactory

from mylabour.model_utils import leave_only_predetermined_number_of_objects

from apps.polls.factories import ChoiceFactory
from apps.polls.models import Poll, Choice, Vote


User = get_user_model()


class PollsManagerSingleUserTest(TestCase):
    """
    Tests for methods of manager "PollsManager", namely, intended for single user.
    (it made for better productivity)
    """

    @classmethod
    def setUpTestData(cls):

        # create user
        cls.user = UserFactory()

    def setUp(self):

        # create a polls with choices
        call_command('factory_test_polls', '4')

        self.poll = Poll.objects.first()
        self.choice = self.poll.choices.first()

        # clear all votes of the user, since i will be changed in next test
        self.user.votes.filter().delete()

    def test_get_report_votes_of_user_if_user_has_no_votes(self):
        self.assertTupleEqual(
            (),
            User.polls.get_report_votes_of_user(self.user)
        )

    def test_get_report_votes_of_user_if_user_has_single_votes(self):
        # add a vote
        self.user.votes.create(poll=self.poll, choice=self.choice)

        self.assertTupleEqual(
            ('Voted for a choice "{0}" in a poll "{1}"'.format(
                self.choice, self.poll
            ), ),
            User.polls.get_report_votes_of_user(self.user)
        )

    def test_get_report_votes_of_user_if_user_has_plenty_votes(self):
        # a list records of report
        report = list()

        # adding votes of the user
        for poll in Poll.objects.iterator():
            # add vote
            choice = poll.choices.first()
            self.user.votes.create(poll=poll, choice=choice)

            # add a record to the report
            record = 'Voted for a choice "{0}" in a poll "{1}"'.format(choice, poll)
            report.append(record)

        report = tuple(report)

        self.assertTupleEqual(
            report,
            User.polls.get_report_votes_of_user(self.user)
        )

    def test_get_count_votes_of_user_if_user_has_no_votes(self):

        self.assertEqual(User.polls.get_count_votes_of_user(self.user), 0)

    def test_get_count_votes_of_user_if_user_has_single_vote(self):

        # add a vote
        self.user.votes.create(poll=self.poll, choice=self.choice)

        self.assertEqual(User.polls.get_count_votes_of_user(self.user), 1)

    def test_get_count_votes_of_user_if_user_has_plenty_votes(self):

        # add votes
        for poll in Poll.objects.iterator():
            choice = poll.choices.first()
            self.user.votes.create(poll=poll, choice=choice)

        self.assertEqual(User.polls.get_count_votes_of_user(self.user), 4)

    def test_get_votes_of_user_if_user_has_no_votes(self):
        self.assertQuerysetEqual(
            User.polls.get_votes_of_user(self.user),
            (),
        )

    def test_get_votes_of_user_if_user_has_single_vote(self):

        # add a vote
        self.user.votes.create(poll=self.poll, choice=self.choice)

        self.assertQuerysetEqual(
            User.polls.get_votes_of_user(self.user),
            map(repr, self.user.votes.all())
        )

    def test_get_votes_of_user_if_user_has_plenty_votes(self):

        # add votes
        for poll in Poll.objects.iterator():
            choice = poll.choices.first()
            self.user.votes.create(poll=poll, choice=choice)

        self.assertQuerysetEqual(
            User.polls.get_votes_of_user(self.user),
            map(repr, self.user.votes.all())
        )

    def test_get_latest_vote_of_user_if_user_has_no_votes(self):

        self.assertIsNone(User.polls.get_latest_vote_of_user(self.user))

    def test_get_latest_vote_of_user_if_user_has_single_vote(self):

        # add a vote
        vote = Vote.objects.create(poll=self.poll, choice=self.choice, user=self.user)

        self.assertEqual(User.polls.get_latest_vote_of_user(self.user), vote)

    def test_get_latest_vote_of_user_if_user_has_plenty_votes(self):

        # add votes
        for poll in Poll.objects.iterator():
            choice = poll.choices.first()
            vote = Vote.objects.create(poll=poll, choice=choice, user=self.user)

        self.assertEqual(User.polls.get_latest_vote_of_user(self.user), vote)

    def test_is_active_voter_if_not_polls(self):

        # now polls is not
        Poll.objects.filter().delete()

        # so he is not an active voter
        self.assertFalse(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_not_in_any_polls_given_that_exists_single_poll(self):

        # now is 1 poll, the user participated in 0
        leave_only_predetermined_number_of_objects(Poll, 1)

        # so he is not an active voter
        self.assertFalse(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_alone_poll(self):

        # now is 1 poll, the user participated in 1
        leave_only_predetermined_number_of_objects(Poll, 1)

        # add a vote
        self.user.votes.create(poll=self.poll, choice=self.choice)

        self.assertTrue(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_not_in_any_polls_given_that_exists_two_polls(self):

        # now is 2 polls, the user participated in 0
        leave_only_predetermined_number_of_objects(Poll, 0)

        self.assertFalse(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_one_poll_given_that_exists_two_polls(self):

        # now is 2 polls, the user participated in 1
        leave_only_predetermined_number_of_objects(Poll, 2)

        # add a vote
        self.user.votes.create(poll=self.poll, choice=self.choice)

        self.assertFalse(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_two_polls_given_that_exists_two_polls(self):

        # now is 2 polls, the user participated in 2
        leave_only_predetermined_number_of_objects(Poll, 2)

        # adding votes of the user
        for poll in Poll.objects.all()[:2]:
            # add vote
            choice = poll.choices.first()
            self.user.votes.create(poll=poll, choice=choice)

        self.assertTrue(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_one_poll_given_that_exists_three_polls(self):

        # now is 3 polls, the user participated in 1
        leave_only_predetermined_number_of_objects(Poll, 3)

        # add a vote
        self.user.votes.create(poll=self.poll, choice=self.choice)

        self.assertFalse(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_two_poll_given_that_exists_three_polls(self):

        # now is 3 polls, the user participated in 2
        leave_only_predetermined_number_of_objects(Poll, 3)

        # adding votes of the user
        for poll in Poll.objects.all()[:2]:
            # add vote
            choice = poll.choices.first()
            self.user.votes.create(poll=poll, choice=choice)

        self.assertTrue(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_one_poll_given_that_exists_four_polls(self):

        # now is 4 polls, the user participated in 1
        leave_only_predetermined_number_of_objects(Poll, 4)

        # add a vote
        self.user.votes.create(poll=self.poll, choice=self.choice)

        self.assertFalse(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_two_polls_given_that_exists_four_polls(self):

        # now is 4 polls, the user participated in 2
        leave_only_predetermined_number_of_objects(Poll, 4)

        # adding votes of the user
        for poll in Poll.objects.all()[:2]:
            # add vote
            choice = poll.choices.first()
            self.user.votes.create(poll=poll, choice=choice)

        self.assertFalse(User.polls.is_active_voter(self.user))

    def test_is_active_voter_if_user_participated_in_three_polls_given_that_exists_four_polls(self):

        # now is 4 polls, the user participated in 3
        leave_only_predetermined_number_of_objects(Poll, 4)

        # adding votes of the user
        for poll in Poll.objects.all()[:3]:
            # add vote
            choice = poll.choices.first()
            self.user.votes.create(poll=poll, choice=choice)

        self.assertTrue(User.polls.is_active_voter(self.user))

    def test_get_half_from_total_count_polls_if_no_polls(self):

        leave_only_predetermined_number_of_objects(Poll, 0)

        self.assertEqual(User.polls._get_half_from_total_count_polls(), 0)

    def test_get_half_from_total_count_polls_if_exist_one_poll(self):

        leave_only_predetermined_number_of_objects(Poll, 1)

        self.assertEqual(User.polls._get_half_from_total_count_polls(), 0)

    def test_get_half_from_total_count_polls_if_exist_two_polls(self):

        leave_only_predetermined_number_of_objects(Poll, 2)

        self.assertEqual(User.polls._get_half_from_total_count_polls(), 1)

    def test_get_half_from_total_count_polls_if_exist_three_polls(self):

        leave_only_predetermined_number_of_objects(Poll, 3)

        self.assertEqual(User.polls._get_half_from_total_count_polls(), 1)


class PollsManagerManyUsersTest(TestCase):
    """
    Tests for methods of manager "PollsManager", namely, intended for many users.
    (it made for better productivity)
    """

    def setUp(self):

        # create users
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.user3 = UserFactory()
        self.user4 = UserFactory()
        self.user5 = UserFactory()

        # create a polls with choices
        call_command('factory_test_polls', '5', '--without-votes')

        # unpack the polls in variables
        self.poll1, self.poll2, self.poll3, self.poll4, self.poll5 = Poll.objects.all()

    def test_get_all_voters_if_no_users(self):

        User.objects.filter().delete()
        self.assertQuerysetEqual(User.polls.get_all_voters(), ())

    def test_get_all_voters_if_exists_users_but_not_votes(self):

        self.assertQuerysetEqual(User.polls.get_all_voters(), ())

    def test_get_all_voters_if_one_user_has_vote(self):

        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        self.assertQuerysetEqual(
            User.polls.get_all_voters(),
            map(repr, (self.user1, ))
        )

    def test_get_all_voters_if_several_users_has_diffrent_number_of_votes(self):

        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user2.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user3.votes.create(poll=self.poll4, choice=self.poll4.choices.first())

        self.assertQuerysetEqual(
            User.polls.get_all_voters(),
            map(repr, (self.user1, self.user2, self.user3))
        )

    def test_get_all_voters_if_several_users_has_equal_number_of_votes(self):

        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.last())
        self.user4.votes.create(poll=self.poll4, choice=self.poll4.choices.last())

        self.assertCountEqual(
            User.polls.get_all_voters(),
            (self.user2, self.user3, self.user4)
        )

    def test_get_all_voters_if_several_users_has_equal_and_diffrent_number_of_votes(self):

        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.last())
        self.user2.votes.create(poll=self.poll4, choice=self.poll4.choices.last())
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.last())
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.last())
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.last())
        self.user4.votes.create(poll=self.poll1, choice=self.poll1.choices.last())
        self.user4.votes.create(poll=self.poll2, choice=self.poll2.choices.last())

        all_voters = User.polls.get_all_voters()

        self.assertEqual(all_voters[0], self.user2)
        self.assertCountEqual(all_voters[1:3], (self.user3, self.user4))
        self.assertEqual(all_voters[3], self.user1)

    def test_get_most_active_voters_if_no_users(self):

        User.objects.filter().delete()
        self.assertQuerysetEqual(User.polls.get_most_active_voters(), ())

    def test_get_most_active_voters_if_exists_users_but_not_polls(self):

        Poll.objects.filter().delete()
        self.assertQuerysetEqual(User.polls.get_most_active_voters(), ())

    def test_get_most_active_voters_if_exists_users_but_not_votes(self):

        self.assertQuerysetEqual(User.polls.get_most_active_voters(), ())

    def test_get_most_active_voters_if_exists_1_poll(self):
        """This test considers an order voters too."""

        self.poll1.delete()
        self.poll2.delete()
        self.poll3.delete()
        self.poll4.delete()

        self.user1.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user2.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        self.assertCountEqual(User.polls.get_most_active_voters(), (self.user1, self.user2))

    def test_get_most_active_voters_if_exists_2_polls(self):
        """This test considers an order voters too."""

        self.poll1.delete()
        self.poll2.delete()
        self.poll3.delete()

        self.user2.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user2.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user3.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user4.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user4.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        most_active_voters = User.polls.get_most_active_voters()

        self.assertCountEqual(most_active_voters[:2], (self.user2, self.user4))

    def test_get_most_active_voters_if_exists_3_polls(self):
        """This test considers an order voters too."""

        self.poll1.delete()
        self.poll2.delete()

        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user1.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user2.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user3.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user4.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user4.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user5.votes.create(poll=self.poll3, choice=self.poll4.choices.first())
        self.user5.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user5.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        most_active_voters = User.polls.get_most_active_voters()

        self.assertCountEqual(most_active_voters[:2], (self.user1, self.user5))
        self.assertCountEqual(most_active_voters[2:4], (self.user2, self.user4))

    def test_get_most_active_voters_if_exists_4_polls(self):
        """This test considers an order voters too."""

        self.poll1.delete()

        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user1.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user2.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user3.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user4.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user4.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user4.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user4.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user5.votes.create(poll=self.poll3, choice=self.poll4.choices.first())
        self.user5.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user5.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        most_active_voters = User.polls.get_most_active_voters()

        self.assertCountEqual(most_active_voters[:2], (self.user1, self.user4))
        self.assertEqual(most_active_voters[2], self.user5)

    def test_get_most_active_voters_if_exists_5_polls(self):

        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user2.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user3.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user3.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user4.votes.create(poll=self.poll5, choice=self.poll5.choices.first())
        self.user5.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user5.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user5.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        self.user5.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        self.user5.votes.create(poll=self.poll5, choice=self.poll5.choices.first())

        self.assertQuerysetEqual(
            User.polls.get_most_active_voters(),
            map(repr, (self.user5, self.user2, self.user3))
        )


class PollManagerTest(TestCase):
    """
    Tests for manager of polls.
    """

    @classmethod
    def setUpTestData(cls):

        # create users
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.user3 = UserFactory()

    def setUp(self):

        # create a polls with choices
        call_command('factory_test_polls', '6', '--without-votes')

        # unpack the polls in variables
        self.poll1, self.poll2, self.poll3, self.poll4, self.poll5, self.poll6 = Poll.objects.all()

    def test_change_status_poll_to_opened(self):

        # set a status of a poll
        self.poll2.status = 'draft'
        self.poll2.full_clean()
        self.poll2.save()
        self.assertEqual(self.poll2.status, 'draft')

        # change status
        Poll.objects.change_status_poll(self.poll2, 'opened')
        self.assertEqual(self.poll2.status, 'opened')

    def test_change_status_poll_to_closed(self):

        # set a status of a poll
        self.poll3.status = 'opened'
        self.poll3.full_clean()
        self.poll3.save()
        self.assertEqual(self.poll3.status, 'opened')

        # change status
        Poll.objects.change_status_poll(self.poll3, 'closed')
        self.assertEqual(self.poll3.status, 'closed')

    def test_change_status_poll_to_draft(self):

        # set a status of a poll
        self.poll1.status = 'closed'
        self.poll1.full_clean()
        self.poll1.save()
        self.assertEqual(self.poll1.status, 'closed')

        # change status
        Poll.objects.change_status_poll(self.poll1, 'draft')
        self.assertEqual(self.poll1.status, 'draft')

    def test_get_statistics_polls_by_status_if_no_polls(self):

        Poll.objects.filter().delete()
        self.assertDictEqual(
            Poll.objects.get_statistics_polls_by_status(),
            {
                'draft': 0,
                'closed': 0,
                'opened': 0,
            }
        )

    def test_get_statistics_polls_by_status_if_polls_exists_with_all_posible_status(self):

        Poll.objects.change_status_poll(self.poll1, 'draft')
        Poll.objects.change_status_poll(self.poll2, 'closed')
        Poll.objects.change_status_poll(self.poll3, 'opened')
        Poll.objects.change_status_poll(self.poll4, 'closed')
        Poll.objects.change_status_poll(self.poll5, 'draft')
        Poll.objects.change_status_poll(self.poll6, 'opened')

        self.assertDictEqual(
            Poll.objects.get_statistics_polls_by_status(),
            {
                Poll.CHOICES_STATUS.opened: 2,
                Poll.CHOICES_STATUS.closed: 2,
                Poll.CHOICES_STATUS.draft: 2,
            }
        )

    def test_get_statistics_polls_by_status_if_opened_polls_does_not_exists(self):

        Poll.objects.change_status_poll(self.poll1, 'closed')
        Poll.objects.change_status_poll(self.poll2, 'draft')
        Poll.objects.change_status_poll(self.poll3, 'draft')
        Poll.objects.change_status_poll(self.poll4, 'closed')
        Poll.objects.change_status_poll(self.poll5, 'draft')
        Poll.objects.change_status_poll(self.poll6, 'draft')

        self.assertDictEqual(
            Poll.objects.get_statistics_polls_by_status(),
            {
                Poll.CHOICES_STATUS.opened: 0,
                Poll.CHOICES_STATUS.closed: 2,
                Poll.CHOICES_STATUS.draft: 4,
            }
        )

    def test_get_average_count_votes_in_polls_if_no_polls(self):

        Poll.objects.filter().delete()
        self.assertEqual(Poll.objects.get_average_count_votes_in_polls(), 0)

    def test_get_average_count_votes_in_polls_if_no_votes(self):

        self.assertEqual(Poll.objects.get_average_count_votes_in_polls(), 0)

    def test_get_average_count_votes_in_polls_if_single_poll_has_votes(self):

        self.poll1.votes.create(choice=self.poll1.choices.last(), user=self.user1)
        self.assertEqual(Poll.objects.get_average_count_votes_in_polls(), 0.167)

    def test_get_average_count_votes_in_polls_if_several_polls_has_votes(self):

        self.poll1.votes.create(choice=self.poll1.choices.last(), user=self.user1)
        self.poll1.votes.create(choice=self.poll1.choices.first(), user=self.user2)
        self.poll1.votes.create(choice=self.poll1.choices.last(), user=self.user3)
        self.poll2.votes.create(choice=self.poll2.choices.first(), user=self.user2)
        self.poll2.votes.create(choice=self.poll2.choices.last(), user=self.user3)
        self.poll3.votes.create(choice=self.poll3.choices.last(), user=self.user1)
        self.poll4.votes.create(choice=self.poll4.choices.last(), user=self.user1)
        self.assertEqual(Poll.objects.get_average_count_votes_in_polls(), 1.167)

    def test_get_average_count_votes_in_polls_if_average_count_votes_is_integer(self):

        self.poll1.votes.create(choice=self.poll1.choices.first(), user=self.user1)
        self.poll2.votes.create(choice=self.poll2.choices.last(), user=self.user2)
        self.poll3.votes.create(choice=self.poll3.choices.first(), user=self.user3)
        self.poll4.votes.create(choice=self.poll4.choices.last(), user=self.user2)
        self.poll5.votes.create(choice=self.poll5.choices.first(), user=self.user1)
        self.poll6.votes.create(choice=self.poll5.choices.first(), user=self.user1)
        self.assertEqual(Poll.objects.get_average_count_votes_in_polls(), 1)

    def test_get_average_count_choices_in_polls_if_no_polls(self):

        Poll.objects.filter().delete()
        self.assertEqual(Poll.objects.get_average_count_choices_in_polls(), 0)

    def test_get_average_count_choices_in_polls_if_no_choices(self):

        Choice.objects.filter().delete()
        self.assertEqual(Poll.objects.get_average_count_choices_in_polls(), 0)

    def test_get_average_count_choices_in_polls_if_single_poll_has_choices(self):

        Choice.objects.filter().delete()
        ChoiceFactory(poll=self.poll1)
        ChoiceFactory(poll=self.poll1)
        ChoiceFactory(poll=self.poll1)
        ChoiceFactory(poll=self.poll1)
        self.poll1.votes.create(choice=self.poll1.choices.last(), user=self.user1)
        self.assertEqual(Poll.objects.get_average_count_choices_in_polls(), 0.667)

    def test_get_average_count_choices_in_polls_if_several_polls_has_votes(self):

        Choice.objects.filter().delete()
        ChoiceFactory(poll=self.poll1)
        ChoiceFactory(poll=self.poll2)
        ChoiceFactory(poll=self.poll2)
        ChoiceFactory(poll=self.poll3)
        ChoiceFactory(poll=self.poll3)
        ChoiceFactory(poll=self.poll3)
        ChoiceFactory(poll=self.poll4)
        ChoiceFactory(poll=self.poll4)
        self.assertEqual(Poll.objects.get_average_count_choices_in_polls(), 1.333)

    def test_get_average_count_choices_in_polls_if_average_count_choices_is_integer(self):

        Choice.objects.filter().delete()
        ChoiceFactory(poll=self.poll1)
        ChoiceFactory(poll=self.poll2)
        ChoiceFactory(poll=self.poll3)
        ChoiceFactory(poll=self.poll4)
        ChoiceFactory(poll=self.poll5)
        ChoiceFactory(poll=self.poll6)
        self.assertEqual(Poll.objects.get_average_count_choices_in_polls(), 1)


class VoteManagerTest(TestCase):
    """ """

    now = timezone.now()

    @classmethod
    def setUpTestData(cls):
        # add users
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.user3 = UserFactory()

        cls.now = timezone.now()

    def setUp(self):

        # create a polls with choices
        call_command('factory_test_polls', '4', '--without-votes')

        # unpack the polls in variables
        self.poll1, self.poll2, self.poll3, self.poll4 = Poll.objects.all()

    def test_get_count_voters_if_non_votes(self):

        self.assertEqual(Vote.objects.get_count_voters(), 0)

    def test_get_count_voters_if_only_one_voter(self):

        # add votes
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.last())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.last())

        self.assertEqual(Vote.objects.get_count_voters(), 1)

    def test_get_count_voters_if_is_many_voters(self):

        # add votes
        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.last())
        self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.last())
        self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.last())
        self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.last())
        self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.last())

        self.assertEqual(Vote.objects.get_count_voters(), 3)

    def test_get_latest_vote_if_no_votes(self):

        self.assertIsNone(Vote.objects.get_latest_vote())

    def test_get_latest_vote_if_exists_one_vote(self):
        vote = self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.last())
        self.assertEqual(Vote.objects.get_latest_vote(), vote)

    def test_get_latest_vote_if_exists_many_vote(self):

        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.last())
        self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.last())
        vote = self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())

        self.assertEqual(Vote.objects.get_latest_vote(), vote)

    def test_get_statistics_count_votes_by_months_for_past_year_if_no_votes(self):
        self.assertListEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ((self.now - relativedelta(months=11)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=10)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=9)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=8)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=7)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=6)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=5)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=4)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=3)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=2)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=1)).strftime('%b %Y'), 0),
                (self.now.strftime('%b %Y'), 0),
            ],
        )

    def test_get_statistics_count_votes_by_months_for_past_year_if_votes_added_rightnow(self):

        self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.last())
        self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        self.user3.votes.create(poll=self.poll2, choice=self.poll2.choices.first())

        self.assertListEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ((self.now - relativedelta(months=11)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=10)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=9)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=8)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=7)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=6)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=5)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=4)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=3)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=2)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=1)).strftime('%b %Y'), 0),
                (self.now.strftime('%b %Y'), 3),
            ],
        )

    def test_get_statistics_count_votes_by_months_for_past_year_if_exists_votes_added_more_than_year_ago(self):

        # tonow
        self.user1.votes.create(poll=self.poll4, choice=self.poll4.choices.last())

        # month ago
        vote = self.user2.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=1))

        # twenty months ago
        vote = self.user3.votes.create(poll=self.poll4, choice=self.poll4.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=20))

        # one month ago
        vote = self.user1.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=1))

        # one month ago
        vote = self.user2.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=1))

        # five months ago
        vote = self.user3.votes.create(poll=self.poll1, choice=self.poll1.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=5))

        # twelve months ago
        vote = self.user1.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=12))

        # seven months ago
        vote = self.user2.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=7))

        # twelve months ago
        vote = self.user3.votes.create(poll=self.poll2, choice=self.poll2.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=12))

        # threeten months ago
        vote = self.user1.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=13))

        # ten months ago
        vote = self.user2.votes.create(poll=self.poll3, choice=self.poll3.choices.first())
        Vote.objects.filter(pk=vote.pk).update(date_voting=self.now - relativedelta(months=10))

        # tonow
        self.user3.votes.create(poll=self.poll3, choice=self.poll3.choices.first())

        self.assertListEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ((self.now - relativedelta(months=11)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=10)).strftime('%b %Y'), 1),
                ((self.now - relativedelta(months=9)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=8)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=7)).strftime('%b %Y'), 1),
                ((self.now - relativedelta(months=6)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=5)).strftime('%b %Y'), 1),
                ((self.now - relativedelta(months=4)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=3)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=2)).strftime('%b %Y'), 0),
                ((self.now - relativedelta(months=1)).strftime('%b %Y'), 3),
                (self.now.strftime('%b %Y'), 2),
            ],
        )

    @mock.patch('django.utils.timezone.now')
    def test_get_statistics_count_votes_by_months_for_past_year_if_now_if_new_year(self, mock_now):

        # make mock for now datetime
        mock_now_datetime = timezone.datetime(year=2010, month=1, day=1, tzinfo=self.now.tzinfo)
        mock_now.return_value = mock_now_datetime

        datetimes_voting = (
            # in this month
            mock_now_datetime,
            # in past month
            timezone.datetime(2009, 12, 31, microsecond=999999, tzinfo=self.now.tzinfo),
            # in past month
            timezone.datetime(2009, 12, 31, tzinfo=self.now.tzinfo),
            # in past month
            timezone.datetime(2009, 12, 1, tzinfo=self.now.tzinfo),
            # two months ago
            timezone.datetime(2009, 11, 30, microsecond=999999, tzinfo=self.now.tzinfo),
            # more year ago
            timezone.datetime(2008, 12, 31, microsecond=999999, tzinfo=self.now.tzinfo),
            # year and day ago
            timezone.datetime(2008, 12, 31, tzinfo=self.now.tzinfo),
            # less year ago
            timezone.datetime(2009, 1, 2, tzinfo=self.now.tzinfo),
            # exact year ago
            timezone.datetime(2009, 1, 1, tzinfo=self.now.tzinfo),
            # less year ago
            timezone.datetime(2009, 1, 31, microsecond=999999, tzinfo=self.now.tzinfo),
            # eleven months ago
            timezone.datetime(2009, 2, 1, tzinfo=self.now.tzinfo),
            # eleven months ago
            timezone.datetime(2009, 2, 1, microsecond=999999, tzinfo=self.now.tzinfo),
        )

        self._add_votes_with_determined_date_voting(datetimes_voting)

        self.assertEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ('Feb 2009', 2),
                ('Mar 2009', 0),
                ('Apr 2009', 0),
                ('May 2009', 0),
                ('Jun 2009', 0),
                ('Jul 2009', 0),
                ('Aug 2009', 0),
                ('Sep 2009', 0),
                ('Oct 2009', 0),
                ('Nov 2009', 1),
                ('Dec 2009', 3),
                ('Jan 2010', 1),
            ]
        )

    @mock.patch('django.utils.timezone.now')
    def test_get_statistics_count_votes_by_months_for_past_year_given_that_past_year_was_leap(self, mock_now):

        # make mock for now datetime
        mock_now_datetime = timezone.datetime(year=2013, month=1, day=31, tzinfo=self.now.tzinfo)
        mock_now.return_value = mock_now_datetime

        # naive datetimes
        datetimes_voting = (
            # in past month
            timezone.datetime(2012, 12, 31, microsecond=999999),
            # in past month
            timezone.datetime(2012, 12, 1),
            # two months ago
            timezone.datetime(2012, 11, 1),
            # two months ago
            timezone.datetime(2012, 11, 30, microsecond=999999),
            # three months ago
            timezone.datetime(2012, 10, 31, microsecond=999999),
            # three months ago
            timezone.datetime(2012, 10, 1),
            # exact year ago
            timezone.datetime(2012, 1, 31),
            # more year ago
            timezone.datetime(2012, 1, 1),
            # nearly year ago
            timezone.datetime(2012, 2, 1),
            # less year ago
            timezone.datetime(2012, 2, 28, microsecond=999999),
            # less year ago
            timezone.datetime(2012, 2, 29, microsecond=999999),
            # more year ago
            timezone.datetime(2011, 12, 31),
        )

        self._add_votes_with_determined_date_voting(datetimes_voting)

        self.assertEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ('Feb 2012', 3),
                ('Mar 2012', 0),
                ('Apr 2012', 0),
                ('May 2012', 0),
                ('Jun 2012', 0),
                ('Jul 2012', 0),
                ('Aug 2012', 0),
                ('Sep 2012', 0),
                ('Oct 2012', 2),
                ('Nov 2012', 2),
                ('Dec 2012', 2),
                ('Jan 2013', 0),
            ]
        )

    @mock.patch('django.utils.timezone.now')
    def test_get_statistics_count_votes_by_months_for_past_year_if_today_last_day_of_month_30(self, mock_now):

        # make mock for now datetime
        mock_now_datetime = timezone.datetime(2016, 9, 30, tzinfo=self.now.tzinfo)
        mock_now.return_value = mock_now_datetime

        # naive datetimes
        datetimes_voting = (
            # in this month
            mock_now_datetime,
            # in this month
            timezone.datetime(2016, 9, 1),
            # in past month
            timezone.datetime(2016, 8, 31, microsecond=999999),
            # in past month
            timezone.datetime(2016, 8, 1),
            # two months ago
            timezone.datetime(2016, 7, 31, microsecond=999999),
            # two months ago
            timezone.datetime(2016, 7, 1),
            # more year ago
            timezone.datetime(2015, 8, 1),
            # more year ago
            timezone.datetime(2015, 8, 31, microsecond=999999),
            # more year ago
            timezone.datetime(2015, 9, 1),
            # exact months ago
            timezone.datetime(2015, 9, 30, microsecond=999999),
            # eleven months ago
            timezone.datetime(2015, 10, 1),
            # eleven months ago
            timezone.datetime(2015, 10, 31, microsecond=999999),
        )

        self._add_votes_with_determined_date_voting(datetimes_voting)

        self.assertEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ('Oct 2015', 2),
                ('Nov 2015', 0),
                ('Dec 2015', 0),
                ('Jan 2016', 0),
                ('Feb 2016', 0),
                ('Mar 2016', 0),
                ('Apr 2016', 0),
                ('May 2016', 0),
                ('Jun 2016', 0),
                ('Jul 2016', 2),
                ('Aug 2016', 2),
                ('Sep 2016', 2),
            ]
        )

    @mock.patch('django.utils.timezone.now')
    def test_get_statistics_count_votes_by_months_for_past_year_if_today_last_day_of_month_31(self, mock_now):

        # make mock for now datetime
        mock_now_datetime = timezone.datetime(2016, 8, 31, tzinfo=self.now.tzinfo)
        mock_now.return_value = mock_now_datetime

        # naive datetimes
        datetimes_voting = (
            # in this month
            mock_now_datetime,
            # in this month
            timezone.datetime(2016, 8, 1),
            # in past month
            timezone.datetime(2016, 7, 31, microsecond=999999),
            # in past month
            timezone.datetime(2016, 7, 1),
            # two months ago
            timezone.datetime(2016, 6, 30, microsecond=999999),
            # two months ago
            timezone.datetime(2016, 6, 1),
            # more year ago
            timezone.datetime(2015, 7, 1),
            # more year ago
            timezone.datetime(2015, 7, 31, microsecond=999999),
            # more year ago
            timezone.datetime(2015, 8, 1),
            # exact months ago
            timezone.datetime(2015, 8, 31, microsecond=999999),
            # eleven months ago
            timezone.datetime(2015, 9, 1),
            # eleven months ago
            timezone.datetime(2015, 9, 30, microsecond=999999),
        )

        self._add_votes_with_determined_date_voting(datetimes_voting)

        self.assertEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ('Sep 2015', 2),
                ('Oct 2015', 0),
                ('Nov 2015', 0),
                ('Dec 2015', 0),
                ('Jan 2016', 0),
                ('Feb 2016', 0),
                ('Mar 2016', 0),
                ('Apr 2016', 0),
                ('May 2016', 0),
                ('Jun 2016', 2),
                ('Jul 2016', 2),
                ('Aug 2016', 2)
            ]
        )

    @mock.patch('django.utils.timezone.now')
    def test_get_statistics_count_votes_by_months_for_past_year_if_today_middle_of_month(self, mock_now):

        # make mock for now datetime
        mock_now_datetime = timezone.datetime(2016, 4, 15, tzinfo=self.now.tzinfo)
        mock_now.return_value = mock_now_datetime

        # naive datetimes
        datetimes_voting = (
            # in this month
            timezone.datetime(2016, 4, 3),
            # in past month
            timezone.datetime(2016, 3, 10),
            # two months ago
            timezone.datetime(2016, 2, 29, microsecond=999999),
            # two months ago
            timezone.datetime(2016, 2, 1),
            # three months ago
            timezone.datetime(2016, 1, 30, microsecond=999999),
            # three months ago
            timezone.datetime(2016, 1, 1),
            # more year ago
            timezone.datetime(2015, 3, 31, microsecond=999999),
            # more year ago
            timezone.datetime(2015, 3, 1),
            # exact year ago
            timezone.datetime(2015, 4, 15),
            # more year ago
            timezone.datetime(2015, 4, 1),
            # less year ago
            timezone.datetime(2015, 4, 30, microsecond=999999),
            # less year ago
            timezone.datetime(2015, 5, 1),
        )

        self._add_votes_with_determined_date_voting(datetimes_voting)

        self.assertEqual(
            Vote.objects.get_statistics_count_votes_by_months_for_past_year(),
            [
                ('May 2015', 1),
                ('Jun 2015', 0),
                ('Jul 2015', 0),
                ('Aug 2015', 0),
                ('Sep 2015', 0),
                ('Oct 2015', 0),
                ('Nov 2015', 0),
                ('Dec 2015', 0),
                ('Jan 2016', 2),
                ('Feb 2016', 2),
                ('Mar 2016', 1),
                ('Apr 2016', 1),
            ]
        )

    def _add_votes_with_determined_date_voting(self, datetimes_voting):
        """An auxillary function for creating votes with determined dates voting."""

        data = (
            (self.user1, self.poll1, self.poll1.choices.last()),
            (self.user1, self.poll2, self.poll2.choices.last()),
            (self.user1, self.poll3, self.poll3.choices.last()),
            (self.user1, self.poll4, self.poll4.choices.last()),
            (self.user2, self.poll1, self.poll1.choices.last()),
            (self.user2, self.poll2, self.poll2.choices.last()),
            (self.user2, self.poll3, self.poll3.choices.last()),
            (self.user2, self.poll4, self.poll4.choices.last()),
            (self.user3, self.poll1, self.poll1.choices.last()),
            (self.user3, self.poll2, self.poll2.choices.last()),
            (self.user3, self.poll3, self.poll3.choices.last()),
            (self.user3, self.poll4, self.poll4.choices.last()),
        )

        if len(datetimes_voting) != len(data):
            raise Exception('Count datetimes for voting is not equal available data.')

        for date_voting, user_poll_choice in zip(datetimes_voting, data):

            # unpack user, poll, choice
            user, poll, choice = user_poll_choice

            # add a current timezone to a naive datetime
            date_voting = date_voting.replace(tzinfo=self.now.tzinfo)

            # create a vote
            vote = Vote.objects.create(user=user, poll=poll, choice=choice)

            # update date voting of the vote
            Vote.objects.filter(pk=vote.pk).update(date_voting=date_voting)
