
from django.core.management import call_command
from django.test import TestCase

from apps.polls.constants import MAX_COUNT_CHOICES_IN_POLL, MIN_COUNT_CHOICES_IN_POLL
from apps.polls.models import Poll, Choice, Vote
from apps.users.factories import UserFactory


class TestCommandFactoryTestPolls(TestCase):
    """ Tests for own app`s commands."""

    count_users = 10

    @classmethod
    def setUpTestData(cls):
        for i in range(cls.count_users):
            UserFactory()

        call_command('factory_test_polls', '10')

    # def test_until_call_command(self):
    #     self.assertEqual(Poll.objects.count(), 0)
    #     self.assertEqual(Choice.objects.count(), 0)
    #     self.assertEqual(Vote.objects.count(), 0)

    def test_count_created_polls(self):
        self.assertEqual(Poll.objects.count(), 10)

    def test_total_count_created_choices(self):
        count_choice = Choice.objects.count()
        self.assertGreaterEqual(count_choice, MAX_COUNT_CHOICES_IN_POLL)
        self.assertLessEqual(count_choice, MIN_COUNT_CHOICES_IN_POLL)

    def test_total_count_created_votes(self):
        self.assertLessEqual(Vote.objects.count(), self.count_users)

    def test_shuffled_dates_of_polls(self):
        self.assertEqual(Poll.objects.count(), 1)

        for date_modified, date_added in Poll.objects.values('date_modified', 'date_added'):
            self.assertGreaterEqual(date_modified, date_added)
