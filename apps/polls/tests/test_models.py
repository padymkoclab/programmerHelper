
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.factories import AccountFactory, levels_accounts_factory
from apps.accounts.models import Account
from apps.polls.models import Poll, Choice, VoteInPoll
from apps.polls.factories import PollFactory, ChoiceFactory


class PollTest(TestCase):
    """
    Tests for polls.
    """

    @classmethod
    def setUpTestData(self):
        levels_accounts_factory()
        for i in range(15):
            AccountFactory(is_active=True)

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

    def test_unique_title(self):
        poll1 = PollFactory(title='В чём лично вы находите преимущество маштабируемости?')
        poll2 = PollFactory(title='В чём, лично вы, находите преимущество маштабируемости?')
        #
        poll1.full_clean()
        poll2.full_clean()
        #
        poll1.title = 'В чём, лично вы, находите преимущество маштабируемости?'
        self.assertRaises(ValidationError, poll1.full_clean)
        poll1.title = 'В чём, лично вы, находите преимущество маштабируемости? '
        poll1.full_clean()
        poll1.save()

    def test_unique_slug_of_poll(self):
        title = 'Как вы оцениваете современные CSS frameworks?'
        upper_title = title.upper()
        lower_title = title.lower()
        title_title = title.title()
        poll1 = PollFactory(title=upper_title)
        poll2 = PollFactory(title=lower_title)
        poll3 = PollFactory(title=title_title)
        #
        poll1.full_clean()
        poll2.full_clean()
        poll3.full_clean()
        #
        self.assertEqual(poll1.slug, slugify(title, allow_unicode=True))
        self.assertEqual(poll2.slug, slugify(title, allow_unicode=True) + '-2')
        self.assertEqual(poll3.slug, slugify(title, allow_unicode=True) + '-3')

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
        superuser = AccountFactory(is_active=True, is_superuser=True)
        #
        self.client.force_login(superuser)
        #
        response = self.client.get(self.poll.get_admin_url())
        self.assertEqual(response.status_code, 200)

    def test_get_most_popular_choice_or_choices_if_does_not_have_choices(self):
        self.assertEqual(self.poll.choices.count(), 0)
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), ())

    def test_get_most_popular_choice_or_choices_if_have_single_choice(self):
        choice = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 1)
        #
        accounts = Account.objects.random_accounts(2)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice)
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), [choice])

    def test_get_most_popular_choice_or_choices_if_have_several_choices_with_equal_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 3)
        #
        accounts = Account.objects.random_accounts(6)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[2], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[3], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[4], poll=self.poll, choice=choice3)
        VoteInPoll.objects.create(account=accounts[5], poll=self.poll, choice=choice3)
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), [choice1, choice2, choice3])

    def test_get_most_popular_choice_or_choices_if_have_several_choices_with_different_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 3)
        #
        accounts = Account.objects.random_accounts(6)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[2], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[3], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[4], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[5], poll=self.poll, choice=choice3)
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), [choice2])

    def test_get_result_poll_if_poll_does_not_have_choices(self):
        self.assertEqual(self.poll.choices.count(), 0)
        self.assertCountEqual(self.poll.get_result_poll(), ())

    def test_get_result_poll_if_poll_have_single_choice(self):
        choice = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 1)
        self.assertCountEqual(self.poll.get_result_poll(), ((choice, 0),))
        #
        accounts = Account.objects.random_accounts(2)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice)
        self.assertCountEqual(self.poll.get_result_poll(), ((choice, 2),))

    def test_get_result_poll_if_poll_have_two_choices_with_equal_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 2)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice1, 0), (choice2, 0))
        )
        #
        accounts = Account.objects.random_accounts(4)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[2], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[3], poll=self.poll, choice=choice2)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice1, 2), (choice2, 2))
        )

    def test_get_result_poll_if_poll_have_two_choices_with_different_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 2)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice1, 0), (choice2, 0))
        )
        #
        accounts = Account.objects.random_accounts(3)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[2], poll=self.poll, choice=choice2)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice1, 2), (choice2, 1))
        )

    def test_get_result_poll_if_poll_have_three_choices_with_equal_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 3)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice1, 0), (choice3, 0), (choice2, 0))
        )
        #
        accounts = Account.objects.random_accounts(9)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[2], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[3], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[4], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[5], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[6], poll=self.poll, choice=choice3)
        VoteInPoll.objects.create(account=accounts[7], poll=self.poll, choice=choice3)
        VoteInPoll.objects.create(account=accounts[8], poll=self.poll, choice=choice3)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice3, 3), (choice1, 3), (choice2, 3))
        )

    def test_get_result_poll_if_poll_have_three_choices_with_different_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 3)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice1, 0), (choice3, 0), (choice2, 0))
        )
        #
        accounts = Account.objects.random_accounts(6)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[2], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[3], poll=self.poll, choice=choice3)
        VoteInPoll.objects.create(account=accounts[4], poll=self.poll, choice=choice3)
        VoteInPoll.objects.create(account=accounts[5], poll=self.poll, choice=choice3)
        self.assertCountEqual(
            self.poll.get_result_poll(),
            ((choice3, 3), (choice1, 2), (choice2, 1))
        )

    def test_get_count_votes_if_not_choices(self):
        self.assertEqual(self.poll.choices.count(), 0)
        self.assertEqual(self.poll.get_count_votes(), 0)

    def test_get_count_votes_with_choices_but_without_votes(self):
        ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 3)
        self.assertEqual(self.poll.get_count_votes(), 0)

    def test_get_count_votes_with_choices_where_single_choice_have_votes(self):
        ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        choice = ChoiceFactory(poll=self.poll)
        #
        accounts = Account.objects.random_accounts(2)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice)
        #
        self.assertEqual(self.poll.choices.count(), 3)
        self.assertEqual(self.poll.get_count_votes(), 2)

    def test_get_count_votes_with_choices_where_all_choices_have_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        #
        accounts = Account.objects.random_accounts(7)
        VoteInPoll.objects.create(account=accounts[0], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[1], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[2], poll=self.poll, choice=choice3)
        VoteInPoll.objects.create(account=accounts[3], poll=self.poll, choice=choice2)
        VoteInPoll.objects.create(account=accounts[4], poll=self.poll, choice=choice3)
        VoteInPoll.objects.create(account=accounts[5], poll=self.poll, choice=choice1)
        VoteInPoll.objects.create(account=accounts[6], poll=self.poll, choice=choice2)
        #
        self.assertEqual(self.poll.choices.count(), 3)
        self.assertEqual(self.poll.get_count_votes(), 7)

    def test_get_count_choices_if_choices_is_not_presents(self):
        self.assertEqual(self.poll.get_count_choices(), 0)

    def test_get_count_choices_if_choices_presents(self):
        ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.get_count_choices(), 2)

    def test_get_voters(self):
        raise NotImplementedError


class ChoiceTest(TestCase):
    """
    Tests for polls.
    """

    @classmethod
    def setUpTestData(self):
        levels_accounts_factory()
        self.account1 = AccountFactory(is_active=True)
        self.account2 = AccountFactory(is_active=True)
        self.account3 = AccountFactory(is_active=True)

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

    def test_unique_error_message_for_text_choice_and_poll(self):
        text_choice = 'Same text as in all'
        choice2 = ChoiceFactory(poll=self.poll, text_choice=text_choice)
        choice2.full_clean()
        choice3 = Choice(poll=self.poll, text_choice=text_choice)
        self.assertRaisesMessage(ValidationError, 'Poll does not have more than one choice with this text', choice3.full_clean)

    def test_get_count_votes(self):
        # no votes
        self.assertEqual(self.choice.get_count_votes(), 0)
        # added votes
        VoteInPoll.objects.create(poll=self.poll, choice=self.choice, account=self.account1)
        VoteInPoll.objects.create(poll=self.poll, choice=self.choice, account=self.account2)
        VoteInPoll.objects.create(poll=self.poll, choice=self.choice, account=self.account3)
        self.assertEqual(self.choice.get_count_votes(), 3)

    def test_get_voters(self):
        raise NotImplementedError


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
        levels_accounts_factory()
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

    def test_unique_account_and_poll(self):
        self.vote = VoteInPoll(poll=self.poll, account=self.account2, choice=self.choice1)
        self.assertRaisesMessage(ValidationError, 'This user already participated in that poll.', self.vote.full_clean)
