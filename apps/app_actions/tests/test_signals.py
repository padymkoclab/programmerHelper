
import random

from django.test import TestCase

# from apps.app_actions.models import Action
from apps.app_accounts.factories import factory_accounts, Factory_Account, factory_account_level
from apps.app_accounts.models import Account
from apps.app_polls.factories import factory_polls
from apps.app_polls.models import Poll, VoteInPoll
from apps.app_articles.factories import factory_articles, Factory_Article
# from apps.app_articles.models import Article
from apps.app_badges.factories import factory_badges
from apps.app_courses.factories import factory_courses
from apps.app_courses.models import Course
from apps.app_solutions.factories import factory_solutions_categories, Factory_Solution
# from apps.app_solutions.models import Solution
from apps.app_tags.factories import factory_tags
from apps.app_snippets.factories import factory_snippets
from apps.app_web_links.factories import factory_web_links
from apps.app_web_links.models import WebLink

from apps.app_actions.signals import *


class BaseTestClass_for_prepopulated_data(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        factory_tags(10)
        factory_web_links(10)
        factory_badges()
        factory_account_level()
        factory_accounts(10)


class TestSignal_Badge_Dispatcher(BaseTestClass_for_prepopulated_data):
    """

    """

    @classmethod
    def setUpTestData(cls):
        super(TestSignal_Badge_Dispatcher, cls).setUpTestData()

        factory_solutions_categories()

        cls.account = Factory_Account()
        for i in range(3):
            article = Factory_Article(author=cls.account)
            article.links.clear()
            article.save()
            solution = Factory_Solution(author=cls.account)
            solution.links.clear()
            solution.save()

    def test_getting_badge_creator_article(self):
        account = Factory_Account()
        Factory_Article(author=account)
        self.assertTrue(account.has_badge('Dispatcher'))

    def test_changing_author_of_article_with_losing_or_acquisition_badge(self):
        new_account = Factory_Account()
        #
        self.assertFalse(self.account.has_badge('Dispatcher'))
        self.assertFalse(new_account.has_badge('Dispatcher'))
        #
        web_links = WebLink.objects.all()[:2]
        solution = self.account.solutions.first()
        solution.links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))
        #
        solution.author = new_account
        solution.save()
        self.assertFalse(self.account.has_badge('Dispatcher'))
        self.assertTrue(new_account.has_badge('Dispatcher'))

    def test_losing_badge_from_creator_after_deleting_article(self):
        account = Factory_Account()
        article = Factory_Article(author=account)
        self.assertTrue(account.has_badge('Dispatcher'))
        article.delete()
        self.assertFalse(account.has_badge('Dispatcher'))

    def test_articles_without_links(self):

        self.assertFalse(self.account.has_badge('Dispatcher'))

    def test_with_alone_article_with_links(self):

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:4]
        self.account.articles.last().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))

    def test_adding_and_removing_links_from_articles(self):

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:2]
        self.account.articles.first().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))
        self.account.articles.first().links.remove(web_links[0])
        self.assertTrue(self.account.has_badge('Dispatcher'))
        self.account.articles.first().links.remove(web_links[1])
        self.assertFalse(self.account.has_badge('Dispatcher'))

    def test_solutions_without_links(self):

        self.assertFalse(self.account.has_badge('Dispatcher'))

    def test_with_alone_solution_with_links(self):

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:3]
        self.account.solutions.last().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))

    def test_adding_and_removing_links_from_solutions(self):

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:2]
        self.account.solutions.last().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))
        self.account.solutions.last().links.remove(web_links[0])
        self.assertTrue(self.account.has_badge('Dispatcher'))
        self.account.solutions.last().links.remove(web_links[1])
        self.assertFalse(self.account.has_badge('Dispatcher'))

    def test_with_links_in_solution_and_article_at_the_same_time(self):
        """ """

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:3]
        self.account.solutions.last().links.add(*web_links)
        self.account.articles.first().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))

    def test_with_links_in_solution_but_no_in_article(self):
        """ """

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:3]
        self.account.solutions.last().links.add(*web_links)
        self.account.articles.first().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))
        self.account.articles.first().links.clear()
        self.assertTrue(self.account.has_badge('Dispatcher'))

    def test_without_links_in_solution_but_in_article(self):
        """ """

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:4]
        self.account.solutions.first().links.add(*web_links)
        self.account.articles.first().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))
        self.account.solutions.first().links.clear()
        self.assertTrue(self.account.has_badge('Dispatcher'))

    def test_without_links_in_solution_and_article_at_the_same_time(self):
        """ """

        self.assertFalse(self.account.has_badge('Dispatcher'))
        web_links = WebLink.objects.all()[:2]
        self.account.solutions.first().links.add(*web_links)
        self.account.articles.first().links.add(*web_links)
        self.assertTrue(self.account.has_badge('Dispatcher'))
        self.account.solutions.first().links.clear()
        self.account.articles.first().links.clear()
        self.assertFalse(self.account.has_badge('Dispatcher'))


class TestSignal_Badge_Sage(BaseTestClass_for_prepopulated_data):
    """

    """

    def setUp(self):
        factory_courses(3)

    def test_getting_badge_members_authorship_of_course(self):
        course = Course.objects.first()
        author = Factory_Account()
        course.authorship.add(author)
        self.assertTrue(author.has_badge('Sage'))
        action = author.actions.latest()
        self.assertEqual(action.flag, 'ADD')
        self.assertEqual(action.message, 'Added as author to the course "{0}".'.format(course))

    def test_losing_badge_after_full_clear_authorship_of_course(self):
        course = Course.objects.last()
        authors = course.authorship.all()
        course.authorship.clear()
        for author in authors:
            self.assertFalse(author.has_badge('Sage'))
            action = author.actions.latest()
            self.assertEqual(action.flag, 'DEL')
            self.assertEqual(action.message, 'Removed as author from the course "{0}".'.format(course))

    def test_getting_badge_after_changed_authorship_of_course(self):
        course = Course.objects.last()
        authors = (Factory_Account(), Factory_Account(), Factory_Account())
        course.authorship.add(*authors)
        for author in authors:
            action = author.actions.latest()
            self.assertEqual(action.flag, 'ADD')
            self.assertEqual(action.message, 'Added as author to the course "{0}".'.format(course))
            self.assertTrue(author.has_badge('Sage'))

    def test_losing_or_getting_badge_after_changed_authorship_of_course(self):
        course = Course.objects.last()
        authors = (Factory_Account(), Factory_Account(), Factory_Account())
        course.authorship.add(*authors)
        course.authorship.remove(*authors)
        for author in authors:
            action = author.actions.latest()
            self.assertEqual(action.flag, 'DEL')
            self.assertEqual(action.message, 'Removed as author from the course "{0}".'.format(course))
            self.assertFalse(author.has_badge('Sage'))

    def test_losing_badge_after_full_clear_courses_of_author(self):
        courses = Course.objects.all()
        author = Factory_Account()
        author.courses.add(*courses)
        author.courses.clear()
        self.assertFalse(author.has_badge('Sage'))
        for i, course in enumerate(courses[::-1]):
            action = author.actions.all()[i]
            self.assertEqual(action.flag, 'DEL')
            self.assertEqual(action.message, 'Removed as author from the course "{0}".'.format(course))

    def test_getting_badge_after_changed_courses_of_author(self):
        course1, course2 = Course.objects.first(), Course.objects.last()
        author = Factory_Account()
        author.courses.add(course1, course2)
        self.assertTrue(author.has_badge('Sage'))
        latest_actions = author.actions.all()[:2]
        for action in latest_actions:
            self.assertEqual(action.flag, 'ADD')
        self.assertIn(action.message, [
            'Added as author to the course "{0}".'.format(course1),
            'Added as author to the course "{0}".'.format(course2),
        ])

    def test_losing_badge_after_changed_courses_of_author(self):
        course1, course2 = Course.objects.first(), Course.objects.last()
        author = Factory_Account()
        author.courses.add(course1, course2)
        # remove first course
        author.courses.remove(course1)
        self.assertTrue(author.has_badge('Sage'))
        latest_action = author.actions.latest()
        self.assertEqual(latest_action.flag, 'DEL')
        self.assertEqual(latest_action.message, 'Removed as author from the course "{0}".'.format(course1))
        # remove first course
        author.courses.remove(course2)
        self.assertFalse(author.has_badge('Sage'))
        latest_action = author.actions.latest()
        self.assertEqual(latest_action.flag, 'DEL')
        self.assertEqual(latest_action.message, 'Removed as author from the course "{0}".'.format(course2))

    def test_losing_badge_members_authorship_of_course_after_deleting_course(self):
        course = Course.objects.last()
        authors = (Factory_Account(), Factory_Account(), Factory_Account())
        course.authorship.add(*authors)
        for author in authors:
            self.assertTrue(author.has_badge('Sage'))
        course.delete()
        for author in authors:
            self.assertFalse(author.has_badge('Sage'))
            latest_action = author.actions.latest()
            self.assertEqual(latest_action.flag, 'DEL')
            self.assertEqual(latest_action.message, 'Removed as author from the course "{0}".'.format(course))


class TestSignal_Badge_Voter(BaseTestClass_for_prepopulated_data):
    """

    """

    def setUp(self):
        factory_polls(2)
        for poll in Poll.objects.iterator():
            if not poll.votes.count():
                for user in Account.objects.all()[:5]:
                    choice = random.choice(poll.choices.all())
                    VoteInPoll.objects.create(poll=poll, user=user, choice=choice)

    def test_getting_badge_voters(self):
        poll = Poll.objects.last()
        for voter in poll.votes.iterator():
            self.assertTrue(voter.has_badge('Voter'))
            action = voter.actions.latest()
            self.assertEqual(action.message, 'Participated in the poll "{0}".'.format(poll))
            self.assertEqual(action.flag, 'ADD')

    def test_getting_badge_after_changed_votes_of_poll(self):
        poll1, poll2 = Poll.objects.first(), Poll.objects.last()
        voter = Factory_Account()
        self.assertFalse(voter.has_badge('Voter'))
        # single poll
        choice = random.choice(poll1.choices.all())
        VoteInPoll.objects.create(poll=poll1, user=voter, choice=choice)
        action = voter.actions.latest()
        self.assertEqual(action.flag, 'ADD')
        self.assertEqual(action.message, 'Participated in the poll "{0}".'.format(poll1))
        self.assertTrue(voter.has_badge('Voter'))
        # another poll
        choice = random.choice(poll2.choices.all())
        VoteInPoll.objects.create(poll=poll2, user=voter, choice=choice)
        action = voter.actions.latest()
        self.assertEqual(action.flag, 'ADD')
        self.assertEqual(action.message, 'Participated in the poll "{0}".'.format(poll2))

    def test_losing_badge_after_changed_votes_of_poll(self):
        poll1, poll2 = Poll.objects.first(), Poll.objects.last()
        voter = Factory_Account()
        self.assertFalse(voter.has_badge('Voter'))
        # remove first poll
        choice1 = random.choice(poll1.choices.all())
        choice2 = random.choice(poll2.choices.all())
        vote1 = VoteInPoll.objects.create(poll=poll1, user=voter, choice=choice1)
        vote2 = VoteInPoll.objects.create(poll=poll2, user=voter, choice=choice2)
        vote1.delete()
        latest_action = voter.actions.latest()
        self.assertEqual(latest_action.flag, 'DEL')
        self.assertEqual(latest_action.message, 'Removed from voters in the poll "{0}".'.format(poll1))
        self.assertTrue(voter.has_badge('Voter'))
        # remove second poll
        vote2.delete()
        latest_action = voter.actions.latest()
        self.assertEqual(latest_action.flag, 'DEL')
        self.assertEqual(latest_action.message, 'Removed from voters in the poll "{0}".'.format(poll2))
        self.assertFalse(voter.has_badge('Voter'))

    def test_losing_badge_after_deleting_poll(self):
        poll = Poll.objects.last()
        choice = random.choice(poll.choices.all())
        voter = Factory_Account()
        VoteInPoll.objects.create(poll=poll, user=voter, choice=choice)
        self.assertTrue(voter.has_badge('Voter'))
        poll.delete()
        self.assertFalse(voter.has_badge('Voter'))
        latest_action = voter.actions.latest()
        self.assertEqual(latest_action.flag, 'DEL')
        self.assertEqual(latest_action.message, 'Removed from voters in the poll "{0}".'.format(poll))


class TestSignal_from_Account(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        factory_account_level()

    def setUp(self):
        self.account = Factory_Account()

    def test_newly_created_the_account(self):
        earliest_action = self.account.actions.earliest()
        self.assertEqual(earliest_action.flag, 'USER')
        self.assertEqual(earliest_action.message, 'Created account.')

    def test_updated_the_account(self):
        self.account.save()
        latest_action = self.account.actions.latest()
        self.assertEqual(latest_action.flag, 'USER')
        self.assertEqual(latest_action.message, 'Updated account.')

    def test_changed_status_the_account_from_active_to_unactive(self):
        self.account.is_active = True
        self.account.save()
        self.account.is_active = False
        self.account.save()
        latest_action = self.account.actions.latest()
        self.assertEqual(latest_action.flag, 'USER')
        self.assertEqual(latest_action.message, 'Account disabled.')

    def test_changed_status_the_account_from_unactive_to_active(self):
        self.account.is_active = False
        self.account.save()
        self.account.is_active = True
        self.account.save()
        latest_action = self.account.actions.latest()
        self.assertEqual(latest_action.flag, 'USER')
        self.assertEqual(latest_action.message, 'Now account is active.')

    def test_changed_status_the_account_from_non_superuser_to_superuser(self):
        self.account.is_superuser = True
        self.account.save()
        latest_action = self.account.actions.latest()
        self.assertEqual(latest_action.flag, 'USER')
        self.assertEqual(latest_action.message, 'Changed status account as superuser.')

    def test_changed_status_the_account_from_superuser_to_non_superuser(self):
        self.account.is_superuser = True
        self.account.save()
        self.account.is_superuser = False
        self.account.save()
        latest_action = self.account.actions.latest()
        self.assertEqual(latest_action.flag, 'USER')
        self.assertEqual(latest_action.message, 'Changed status account as non superuser.')

    # def test_deleted_the_account(self):
    #     self.account.delete()
    #     latest_action = self.account.actions.latest()
    #     self.assertEqual(latest_action.flag, 'USER')
    #     self.assertEqual(latest_action.message, 'Deleted account.')


class TestSignal_Badge_Clear_Heard(BaseTestClass_for_prepopulated_data):
    """

    """

    def setUp(self):
        factory_snippets(1)

    def test_getting_badge_clear_mind(self):
        import ipdb; ipdb.set_trace()
