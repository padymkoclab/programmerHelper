
from django.db import models
from django.core.management import call_command
from django.test import TestCase

from apps.polls.constants import MAX_COUNT_CHOICES_IN_POLL, MIN_COUNT_CHOICES_IN_POLL
from apps.polls.models import Poll, Choice, Vote
from apps.users.factories import UserFactory


class TestCommandFactoryTestPolls(TestCase):
    """
    Tests for own app`s command - "factory_test_polls", with required arguments.
    """

    count_users = 10
    count_polls = 10

    @classmethod
    def setUpTestData(cls):
        for i in range(cls.count_users):
            UserFactory()

        call_command('factory_test_polls', str(cls.count_polls))

    def test_count_created_polls(self):
        self.assertEqual(Poll.objects.count(), self.count_polls)

    def test_total_count_created_choices(self):
        count_choices = Choice.objects.count()
        self.assertGreaterEqual(count_choices, self.count_polls * MIN_COUNT_CHOICES_IN_POLL)
        self.assertLessEqual(count_choices, self.count_polls * MAX_COUNT_CHOICES_IN_POLL)

    def test_count_choices_in_an_each_poll(self):
        polls_with_count_choices = Poll.objects.polls_with_count_choices().values('count_choices')
        max_and_max_count_choices = polls_with_count_choices.aggregate(
            min_count_choices=models.Min('count_choices'),
            max_count_choices=models.Max('count_choices'),
        )
        self.assertGreaterEqual(max_and_max_count_choices['min_count_choices'], MIN_COUNT_CHOICES_IN_POLL)
        self.assertLessEqual(max_and_max_count_choices['max_count_choices'], MAX_COUNT_CHOICES_IN_POLL)

    def test_total_count_created_votes(self):
        """ """

        self.assertGreater(Vote.objects.count(), 1)

    def test_count_choices_of_an_each_poll(self):
        """Chech up, what in a each poll a date_added is less or equal date_modified"""

        self.assertTrue(
            all(
                date_added <= date_modified
                for date_added, date_modified in Poll.objects.values_list('date_added', 'date_modified')
            )
        )

    def test_shuffled_dates_of_polls(self):
        """Chech up, what in a each poll a date_added is less or equal date_modified"""

        self.assertTrue(
            all(
                date_added <= date_modified
                for date_added, date_modified in Poll.objects.values_list('date_added', 'date_modified')
            )
        )

    def test_date_voting_all_votes_of_poll_must_be_great_than_date_added_this_poll(self):
        """ """

        self.assertTrue(all(
            date_voting > poll__date_added
            for date_voting, poll__date_added in Vote.objects.values_list('date_voting', 'poll__date_added')
        ))


class TestCommandFactoryTestPollsWithoutVotes(TestCase):
    """
    Tests for own app`s command - "factory_test_polls", with not required arguments.
    """

    count_polls = 5

    def test_creating_polls_and_choices_without_votes(self):
        call_command('factory_test_polls', str(self.count_polls), '--without-votes')

        # chech up number of polls
        self.assertEqual(Poll.objects.count(), self.count_polls)

        # chech up number of choices
        count_choices = Choice.objects.count()
        self.assertLessEqual(count_choices, self.count_polls * MAX_COUNT_CHOICES_IN_POLL)
        self.assertGreaterEqual(count_choices, self.count_polls * MIN_COUNT_CHOICES_IN_POLL)

        # check up number of votes
        self.assertEqual(Vote.objects.count(), 0)
