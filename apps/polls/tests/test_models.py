
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.users.factories import UserFactory
from utils.django.datetime_utils import convert_date_to_django_date_format

from apps.polls.models import Poll, Choice, Vote
from apps.polls.factories import PollFactory, ChoiceFactory


User = get_user_model()


class PollTest(TestCase):
    """
    Tests for polls.
    """

    @classmethod
    def setUpTestData(self):
        for i in range(7):
            UserFactory(is_active=True)

        self.user1 = UserFactory(is_active=True)
        self.user2 = UserFactory(is_active=True)
        self.user3 = UserFactory(is_active=True)

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

    def test_str(self):
        title = 'Почему так важно уметь думать самому?'
        poll = PollFactory(title=title)
        self.assertEqual(str(poll), title)

    def test_get_absolute_url(self):
        response = self.client.get(self.poll.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_admin_url(self):
        #
        superuser = UserFactory(is_active=True, is_superuser=True)
        #
        self.client.force_login(superuser)
        #
        response = self.client.get(self.poll.get_admin_url())
        self.assertEqual(response.status_code, 200)

    def test_natural_key(self):
        title = 'Почему программист должен знать очень много?'
        poll = PollFactory(title=title)
        self.assertEqual(poll.natural_key(), title)

    def test_get_most_popular_choice_or_choices_if_does_not_have_choices(self):
        self.assertEqual(self.poll.choices.count(), 0)
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), ())

    def test_get_most_popular_choice_or_choices_if_have_single_choice(self):
        choice = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 1)
        #
        users = User.objects.random_users(2)
        Vote.objects.create(user=users[0], poll=self.poll, choice=choice)
        Vote.objects.create(user=users[1], poll=self.poll, choice=choice)
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), [choice])

    def test_get_most_popular_choice_or_choices_if_have_several_choices_with_equal_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 3)
        #
        users = User.objects.random_users(6)
        Vote.objects.bulk_create([
            Vote(user=users[0], poll=self.poll, choice=choice1),
            Vote(user=users[1], poll=self.poll, choice=choice1),
            Vote(user=users[2], poll=self.poll, choice=choice2),
            Vote(user=users[3], poll=self.poll, choice=choice2),
            Vote(user=users[4], poll=self.poll, choice=choice3),
            Vote(user=users[5], poll=self.poll, choice=choice3),
        ])
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), [choice1, choice2, choice3])

    def test_get_most_popular_choice_or_choices_if_have_several_choices_with_different_count_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 3)
        #
        users = User.objects.random_users(6)
        Vote.objects.bulk_create([
            Vote(user=users[0], poll=self.poll, choice=choice1),
            Vote(user=users[1], poll=self.poll, choice=choice1),
            Vote(user=users[2], poll=self.poll, choice=choice2),
            Vote(user=users[3], poll=self.poll, choice=choice2),
            Vote(user=users[4], poll=self.poll, choice=choice2),
            Vote(user=users[5], poll=self.poll, choice=choice3),
        ])
        self.assertCountEqual(self.poll.get_most_popular_choice_or_choices(), [choice2])

    def test_get_result_poll_if_poll_does_not_have_choices(self):
        self.assertEqual(self.poll.choices.count(), 0)
        self.assertCountEqual(self.poll.get_result_poll(), ())

    def test_get_result_poll_if_poll_have_single_choice(self):
        choice = ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.choices.count(), 1)
        self.assertCountEqual(self.poll.get_result_poll(), ((choice, 0),))
        #
        users = User.objects.random_users(2)
        Vote.objects.create(user=users[0], poll=self.poll, choice=choice)
        Vote.objects.create(user=users[1], poll=self.poll, choice=choice)
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
        users = User.objects.random_users(4)
        Vote.objects.bulk_create([
            Vote(user=users[0], poll=self.poll, choice=choice1),
            Vote(user=users[1], poll=self.poll, choice=choice1),
            Vote(user=users[2], poll=self.poll, choice=choice2),
            Vote(user=users[3], poll=self.poll, choice=choice2),
        ])
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
        users = User.objects.random_users(3)
        Vote.objects.bulk_create([
            Vote(user=users[0], poll=self.poll, choice=choice1),
            Vote(user=users[1], poll=self.poll, choice=choice1),
            Vote(user=users[2], poll=self.poll, choice=choice2),
        ])
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
        users = User.objects.random_users(9)
        Vote.objects.bulk_create([
            Vote(user=users[0], poll=self.poll, choice=choice1),
            Vote(user=users[1], poll=self.poll, choice=choice1),
            Vote(user=users[2], poll=self.poll, choice=choice1),
            Vote(user=users[3], poll=self.poll, choice=choice2),
            Vote(user=users[4], poll=self.poll, choice=choice2),
            Vote(user=users[5], poll=self.poll, choice=choice2),
            Vote(user=users[6], poll=self.poll, choice=choice3),
            Vote(user=users[7], poll=self.poll, choice=choice3),
            Vote(user=users[8], poll=self.poll, choice=choice3),
        ])
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
        users = User.objects.random_users(6)
        Vote.objects.bulk_create([
            Vote(user=users[0], poll=self.poll, choice=choice1),
            Vote(user=users[1], poll=self.poll, choice=choice1),
            Vote(user=users[2], poll=self.poll, choice=choice2),
            Vote(user=users[3], poll=self.poll, choice=choice3),
            Vote(user=users[4], poll=self.poll, choice=choice3),
            Vote(user=users[5], poll=self.poll, choice=choice3),
        ])
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
        users = User.objects.random_users(2)
        Vote.objects.create(user=users[0], poll=self.poll, choice=choice)
        Vote.objects.create(user=users[1], poll=self.poll, choice=choice)
        #
        self.assertEqual(self.poll.choices.count(), 3)
        self.assertEqual(self.poll.get_count_votes(), 2)

    def test_get_count_votes_with_choices_where_all_choices_have_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        choice3 = ChoiceFactory(poll=self.poll)
        #
        users = User.objects.random_users(7)
        Vote.objects.bulk_create([
            Vote(user=users[0], poll=self.poll, choice=choice1),
            Vote(user=users[1], poll=self.poll, choice=choice2),
            Vote(user=users[2], poll=self.poll, choice=choice3),
            Vote(user=users[3], poll=self.poll, choice=choice2),
            Vote(user=users[4], poll=self.poll, choice=choice3),
            Vote(user=users[5], poll=self.poll, choice=choice1),
            Vote(user=users[6], poll=self.poll, choice=choice2),
        ])
        #
        self.assertEqual(self.poll.choices.count(), 3)
        self.assertEqual(self.poll.get_count_votes(), 7)

    def test_get_count_choices_if_choices_is_not_presents(self):
        self.assertEqual(self.poll.get_count_choices(), 0)

    def test_get_count_choices_if_choices_presents(self):
        ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        self.assertEqual(self.poll.get_count_choices(), 2)

    def test_get_voters_if_non_choices(self):
        self.assertFalse(self.poll.get_voters().exists())

    def test_get_voters_if_is_choices_but_not_votes(self):
        ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        self.assertFalse(self.poll.get_voters().exists())

    def test_get_voters_if_is_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        Vote.objects.bulk_create([
            Vote(poll=self.poll, choice=choice1, user=self.user1),
            Vote(poll=self.poll, choice=choice1, user=self.user2),
            Vote(poll=self.poll, choice=choice2, user=self.user3),
        ])
        self.assertCountEqual(self.poll.get_voters(), [self.user1, self.user2, self.user3])

    def test_get_date_lastest_voting_if_no_choices(self):
        self.assertIsNone(self.poll.get_date_lastest_voting())

    def test_get_date_lastest_voting_if_is_choices_without_votes(self):
        ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        self.assertIsNone(self.poll.get_date_lastest_voting())

    def test_get_date_lastest_voting_if_is_choices_with_votes(self):
        choice1 = ChoiceFactory(poll=self.poll)
        choice2 = ChoiceFactory(poll=self.poll)
        Vote.objects.bulk_create([
            Vote(poll=self.poll, choice=choice2, user=self.user1),
            Vote(poll=self.poll, choice=choice1, user=self.user2),
        ])
        vote3 = Vote.objects.create(poll=self.poll, choice=choice2, user=self.user3)

        date_voting = convert_date_to_django_date_format(vote3.date_voting)

        self.assertEqual(self.poll.get_date_lastest_voting(), date_voting)


class ChoiceTest(TestCase):
    """
    Tests for polls.
    """

    @classmethod
    def setUpTestData(self):
        self.user1 = UserFactory(is_active=True)
        self.user2 = UserFactory(is_active=True)
        self.user3 = UserFactory(is_active=True)

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

    def test_str(self):
        text_choice = 'Думать самому значит нести ответственность за самого себя'
        choice = ChoiceFactory(text_choice=text_choice, poll=self.poll)
        self.assertEqual(str(choice), text_choice)

    def test_unique_error_message_for_text_choice_and_poll(self):
        text_choice = 'The same text as in all polls'
        choice2 = ChoiceFactory(poll=self.poll, text_choice=text_choice)
        choice2.full_clean()
        choice3 = Choice(poll=self.poll, text_choice=text_choice)
        self.assertRaisesMessage(
            ValidationError,
            'Poll does not have more than one choice with this text',
            choice3.full_clean
        )

    def test_natural_key(self):
        title = 'Сколько боли может выдержать свободный человек?'
        text_choice = 'Да на убой, на как баранов, но если кто-то сможет прорваться, то ...'
        poll = PollFactory(title=title)
        choice = ChoiceFactory(poll=poll, text_choice=text_choice)
        self.assertTupleEqual(choice.natural_key(), (title, text_choice))

    def test_get_count_votes_if_non_votes(self):
        self.assertEqual(self.choice.get_count_votes(), 0)

    def test_get_count_votes_if_is_votes(self):
        Vote.objects.bulk_create([
            Vote(poll=self.poll, choice=self.choice, user=self.user1),
            Vote(poll=self.poll, choice=self.choice, user=self.user2),
            Vote(poll=self.poll, choice=self.choice, user=self.user3),
        ])
        self.assertEqual(self.choice.get_count_votes(), 3)

    def test_get_voters_if_non_voters(self):
        self.assertFalse(self.choice.get_voters().exists())

    def test_get_voters_if_is_voters(self):
        Vote.objects.bulk_create([
            Vote(poll=self.poll, choice=self.choice, user=self.user1),
            Vote(poll=self.poll, choice=self.choice, user=self.user2),
            Vote(poll=self.poll, choice=self.choice, user=self.user3),
        ])
        self.assertCountEqual(self.choice.get_voters(), [self.user1, self.user2, self.user3])

    def test_get_truncated_text_choice_if_length_of_text_choice_is_more_90(self):
        self.choice.text_choice = 'Since it may be happen.' * 8
        self.choice.full_clean()
        self.choice.save()
        self.assertEqual(len(self.choice.text_choice), 184)

        #
        text_choice = ('Since it may be happen.' * 8)[:87] + '...'
        self.assertEqual(self.choice.get_truncated_text_choice(), text_choice)

    def test_get_truncated_text_choice_if_length_of_text_choice_is_equal_90(self):
        self.choice.text_choice = 'Since it may be happen.' * 5
        self.choice.text_choice = self.choice.text_choice[:90]
        self.choice.full_clean()
        self.choice.save()
        self.assertEqual(len(self.choice.text_choice), 90)

        #
        text_choice = ('Since it may be happen.' * 5)[:90]
        self.assertEqual(self.choice.get_truncated_text_choice(), text_choice)


class VoteTest(TestCase):
    """
    Tests for model Vote.
    """

    @classmethod
    def setUpTestData(self):
        self.poll = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.choice1 = ChoiceFactory(poll=self.poll)
        self.choice2 = ChoiceFactory(poll=self.poll)
        self.choice3 = ChoiceFactory(poll=self.poll)
        self.user1 = UserFactory(is_active=True)
        self.user2 = UserFactory(is_active=True)

    def setUp(self):
        self.vote = Vote(poll=self.poll, user=self.user2, choice=self.choice3)
        self.vote.full_clean()
        self.vote.save()

    def test_add_vote(self):
        vote = Vote(poll=self.poll, user=self.user1, choice=self.choice1)
        vote.full_clean()
        vote.save()

    def test_change_vote(self):
        self.vote.choice = self.choice2
        self.vote.full_clean()
        self.vote.save()

    def test_delete_vote(self):
        self.vote.delete()

    def test_str(self):
        self.assertEqual(
            self.vote.__str__(),
            'Vote of a user "{0}" in a poll "{1}"'.format(self.vote.user, self.vote.poll)
        )

    def test_unique_user_and_poll(self):
        self.vote = Vote(poll=self.poll, user=self.user2, choice=self.choice1)
        self.assertRaisesMessage(
            ValidationError, 'This user already participated in that poll.', self.vote.full_clean
        )

    def test_natural_key(self):

        poll = PollFactory()
        choice = ChoiceFactory()
        user = UserFactory()
        vote = Vote.objects.create(user=user, poll=poll, choice=choice)

        self.assertTupleEqual(vote.natural_key(), (poll.natural_key(), user.natural_key(), choice.natural_key()))

    def test_get_truncated_text_choice_if_length_of_text_choice_is_more_90(self):
        self.vote.choice.text_choice = 'Since it may be happen.' * 8
        self.vote.choice.full_clean()
        self.vote.choice.save()
        self.assertEqual(len(self.vote.choice.text_choice), 184)

        #
        text_choice = ('Since it may be happen.' * 8)[:67] + '...'
        self.assertEqual(self.vote.get_truncated_text_choice(), text_choice)

    def test_get_truncated_text_choice_if_length_of_text_choice_is_equal_90(self):
        self.vote.choice.text_choice = 'Since it may be happen.' * 5
        self.vote.choice.text_choice = self.vote.choice.text_choice[:70]
        self.vote.choice.full_clean()
        self.vote.choice.save()
        self.assertEqual(len(self.vote.choice.text_choice), 70)

        #
        text_choice = ('Since it may be happen.' * 5)[:70]
        self.assertEqual(self.vote.get_truncated_text_choice(), text_choice)
