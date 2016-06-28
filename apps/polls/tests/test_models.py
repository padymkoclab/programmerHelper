
from django.test import TestCase

from apps.accounts.factories import AccountFactory, account_level_factory
from apps.polls.models import Poll, Choice, VoteInPoll
from apps.polls.factories import PollFactory, ChoiceFactory


class PollTest(TestCase):
    """
    Tests for polls.
    """

    def setUp(self):
        self.poll = PollFactory()
        self.poll.full_clean()

    def test_create_opened_poll(self):
        data = dict(
            title='Who is who?',
            description='Us very interesting - who are you?',
            status=Poll.CHOICES_STATUS.opened,
        )
        poll = Poll(**data)
        poll.full_clean()
        poll.save()
        self.assertEqual(poll.title, data['title'])
        self.assertEqual(poll.status, data['status'])
        self.assertEqual(poll.description, data['description'])

    def test_create_closed_poll(self):
        data = dict(
            title='I you liked our website?',
            description='Us very interesting you opinion about quality our site?',
            status=Poll.CHOICES_STATUS.closed,
        )
        poll = Poll(**data)
        poll.full_clean()
        poll.save()
        self.assertEqual(poll.title, data['title'])
        self.assertEqual(poll.status, data['status'])
        self.assertEqual(poll.description, data['description'])

    def test_create_draft_poll(self):
        """Test creating draft poll."""

        data = dict(
            title='Where do you live?',
            description='Now, we collecting location information about a visitors our site. And so, where you is?',
            status=Poll.CHOICES_STATUS.draft,
        )
        poll = Poll(**data)
        poll.full_clean()
        poll.save()
        self.assertEqual(poll.title, data['title'])
        self.assertEqual(poll.status, data['status'])
        self.assertEqual(poll.description, data['description'])

    def test_update_poll(self):
        data = dict(
            title='What do you think about new design of the website?',
            description='As you see, after little delay, we given you new version of our website.',
            status=Poll.CHOICES_STATUS.opened,
        )
        poll = Poll(**data)
        poll.full_clean()
        poll.save()
        self.assertEqual(poll.title, data['title'])
        self.assertEqual(poll.status, data['status'])
        self.assertEqual(poll.description, data['description'])

    def test_delete_poll(self):
        self.poll.delete()

    def test_get_absolute_url(self):
        response = self.client.get(self.poll.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_admin_url(self):
        #
        account_level_factory()
        superuser = AccountFactory(is_active=True, is_superuser=True)
        #
        self.client.force_login(superuser)
        #
        response = self.client.get(self.poll.get_admin_url())
        self.assertEqual(response.status_code, 200)


class ChoiceTest(TestCase):
    """
    Tests for polls.
    """

    def setUp(self):
        self.poll = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.poll.full_clean()
        self.choice = ChoiceFactory(poll=self.poll)
        self.choice.full_clean()

    def test_create_choice(self):
        data = dict(
            poll=self.poll,
            text_choice='16',
        )
        choice = Choice(**data)
        choice.full_clean()
        choice.save()
        self.assertEqual(choice.poll, data['poll'])
        self.assertEqual(choice.text_choice, data['text_choice'])

    def test_update_choice(self):
        data = dict(
            poll=PollFactory(status=Poll.CHOICES_STATUS.opened),
            text_choice='16',
        )
        self.choice.poll = data['poll']
        self.choice.text_choice = data['text_choice']
        self.choice.full_clean()
        self.choice.save()
        self.assertEqual(self.choice.poll, data['poll'])
        self.assertEqual(self.choice.text_choice, data['text_choice'])

    def test_delete_choice(self):
        self.choice.delete()


# @unittest.skip('For some reasons not working')
class VoteInPollTest(TestCase):
    """
    Tests for model VoteInPoll.
    """

    @classmethod
    def setUpTestData(self):
        self.poll = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.choice1 = ChoiceFactory(poll=self.poll)
        self.choice2 = ChoiceFactory(poll=self.poll)
        self.choice3 = ChoiceFactory(poll=self.poll)
        account_level_factory()
        self.account1 = AccountFactory(is_active=True)
        self.account2 = AccountFactory(is_active=True)

    def setUp(self):
        self.vote = VoteInPoll(poll=self.poll, account=self.account2, choice=self.choice3)
        self.vote.full_clean()
        self.vote.save()

    def test_add_vote(self):
        vote = VoteInPoll(poll=self.poll, account=self.account1, choice=self.choice1)
        vote.full_clean()
        vote.save()

    def test_change_vote(self):
        self.vote.choice = self.choice2
        self.vote.full_clean()
        self.vote.save()

    def test_delete_vote(self):
        self.vote.delete()

    def test_string_representation(self):
        self.assertEqual(
            self.vote.__str__(),
            'Vote of a user "{0}" in a poll "{1}"'.format(self.vote.account, self.vote.poll)
        )
