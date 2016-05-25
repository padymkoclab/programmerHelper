
import random

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.app_actions.models import Action
from apps.app_accounts.factories import factory_accounts, Factory_Account, factory_account_level
from apps.app_polls.factories import factory_polls
from apps.app_polls.models import Poll, VoteInPoll
from apps.app_articles.factories import factory_articles, Factory_Article
from apps.app_articles.models import Article
from apps.app_badges.factories import factory_badges
from apps.app_courses.factories import factory_courses
from apps.app_courses.models import Course
from apps.app_solutions.factories import factory_solutions_categories, Factory_Solution
from apps.app_solutions.models import Solution
from apps.app_tags.factories import factory_tags
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

    @classmethod
    def setUpTestData(cls):
        super(TestSignal_Badge_Sage, cls).setUpTestData()
        factory_courses(2)

    def test_getting_badge_members_authorship_of_course(self):
        factory_courses(1)
        last_course = Course.objects.order_by('-date_added').first()
        for author in last_course.authorship.all():
            self.assertTrue(author.has_badge('Sage'))

    def test_losing_or_getting_badge_after_changed_authorship(self):
        # test as reversed
        course = Course.objects.first()
        #
        new_author = Factory_Account()
        course.authorship.add(new_author)
        self.assertTrue(new_author.has_badge('Sage'))
        course.authorship.clear()
        self.assertFalse(new_author.has_badge('Sage'))
        #
        account = Factory_Account()
        course.authorship.add(account)
        self.assertTrue(account.has_badge('Sage'))
        course.authorship.remove(account)
        self.assertFalse(account.has_badge('Sage'))
        # test as not reversed
        course = Course.objects.last()
        author = course.authorship.last()
        self.assertTrue(author.has_badge('Sage'))
        author.courses.clear()
        self.assertFalse(author.has_badge('Sage'))

    def test_losing_badge_members_authorship_of_course_after_deleting_course(self):
        factory_courses(1)
        last_course = Course.objects.order_by('-date_added').first()
        authors = last_course.authorship.all()
        for author in authors:
            self.assertTrue(author.has_badge('Sage'))
        last_course.delete()
        for author in authors:
            self.assertFalse(author.has_badge('Sage'))


class TestSignal_Badge_Voter(BaseTestClass_for_prepopulated_data):
    """

    """

    @classmethod
    def setUpTestData(cls):
        super(TestSignal_Badge_Voter, cls).setUpTestData()
        factory_polls(1)
        poll = Poll.objects.get()
        if not poll.votes.count():
            for user in get_user_model().objects.all()[:5]:
                choice = random.choice(poll.choices.all())
                VoteInPoll.objects.create(poll=poll, user=user, choice=choice)

    def test_getting_badge_voters(self):
        poll = Poll.objects.get()
        for voter in poll.votes.iterator():
            self.assertTrue(voter.has_badge('Voter'))

    def test_losing_or_getting_badge_after_changed_votes_of_poll(self):
        poll = Poll.objects.get()
        voter = poll.votes.first()
        self.assertTrue(voter.has_badge('Voter'))
        vote = VoteInPoll.objects.get(poll=poll, user=voter)
        vote.delete()
        self.assertFalse(voter.has_badge('Voter'))

    def test_losing_badge_after_deleteing_poll(self):
        factory_polls(1)
        poll = Poll.objects.order_by('-date_added').first()
        if not poll.votes.count():
            for user in get_user_model().objects.all()[:5]:
                choice = random.choice(poll.choices.all())
                VoteInPoll.objects.create(poll=poll, user=user, choice=choice)
        voter = poll.votes.last()
        self.assertTrue(voter.has_badge('Voter'))
        poll.delete()
        self.assertFalse(voter.has_badge('Voter'))
