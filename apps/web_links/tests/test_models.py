
import unittest

from django.test import TestCase

from apps.solutions.factories import SolutionFactory, solutions_categories_factory
from apps.articles.factories import ArticleFactory
from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory

from apps.web_links.factories import WebLinkFactory
from apps.web_links.models import WebLink
from mylabour.utils import has_connect_to_internet


class WebLinkTest(TestCase):
    """
    Tests for model of web links.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        badges_factory()
        accounts_factory(15)
        solutions_categories_factory()
        web_links_factory(20)

    def setUp(self):
        self.weblink = WebLinkFactory()

    def test_create_weblink(self):
        data = dict(
            title='Как работать с mock для тестирования Python и Django.',
            url='https://habrahabr.ru/post/141209/',
        )
        weblink = WebLink(**data)
        weblink.full_clean()
        weblink.save()
        self.assertEqual(data['title'], weblink.title)
        self.assertEqual(data['url'], weblink.url)

    def test_update_weblink(self):
        data = dict(
            title='SQL. Function to working with degrees.',
            url='http://www.tutorialspoint.com/sql/sql-numeric-functions.htm#function_degrees',
        )
        self.weblink.title = data['title']
        self.weblink.url = data['url']
        self.weblink.full_clean()
        self.weblink.save()
        self.assertEqual(data['title'], self.weblink.title)
        self.assertEqual(data['url'], self.weblink.url)

    def test_delete_weblink(self):
        self.weblink.delete()

    def test_show_as_str(self):
        # if title is not empty string
        self.weblink.title = 'Page from django docs'
        self.weblink.url = 'https://docs.djangoproject.com/ja/1.9/ref/models/expressions/#writing-your-own-query-expressions'
        self.weblink.full_clean()
        self.weblink.save()
        self.assertIsNotNone(self.weblink.title)
        self.assertEqual(self.weblink.__str__(), 'Page from django docs')
        # if title is empty string
        self.weblink.title = ''
        self.weblink.full_clean()
        self.weblink.save()
        self.assertEqual(self.weblink.__str__(), 'https://docs.djangoproject.com/ja/1.9/ref/model...')

    def test_save_url_in_lowercase(self):
        url1 = WebLinkFactory(url='HTTP://127.0.0.1:8000/ADMIN/WEB_LINKS/WEBLINK/')
        url2 = WebLinkFactory(url='http://www.oreilly.com/pub/e/3712')
        url3 = WebLinkFactory(url='http://Stackoverflow.com/search?Q=CAST+CONVERT+SQl')
        self.assertEqual(url1.url, 'http://127.0.0.1:8000/admin/web_links/weblink/')
        self.assertEqual(url2.url, 'http://www.oreilly.com/pub/e/3712')
        self.assertEqual(url3.url, 'http://stackoverflow.com/search?q=cast+convert+sql')

    @unittest.skipIf(not has_connect_to_internet(), 'Problem with connect to internet.')
    def test_get_status_if_is_connect_internet(self):

        # untested at all

        #
        self.weblink.url = 'https://google.com/'
        self.weblink.full_clean()
        self.weblink.save()
        self.assertTrue(self.weblink.get_status())
        #
        self.weblink.url = 'https://www.this-web-site-does-not-exist.com/it-is-page-does-not-exist.html'
        self.weblink.full_clean()
        self.weblink.save()
        self.assertFalse(self.weblink.get_status())

    @unittest.skipIf(has_connect_to_internet(), 'Test executed because not connect to internet.')
    def test_get_status_if_not_connect_internet(self):

        self.weblink.url = 'https://google.com/'
        self.weblink.full_clean()
        self.weblink.save()
        self.assertIsNone(self.weblink.get_status())
        #
        self.weblink.url = 'https://www.this-web-site-does-not-exist.com/it-is-page-does-not-exist.html'
        self.weblink.full_clean()
        self.weblink.save()
        self.assertIsNone(self.weblink.get_status())

    def test_where_used(self):
        #
        self.assertSequenceEqual(self.weblink.where_used(), ())
        #
        solution1, solution2, solution3 = SolutionFactory(), SolutionFactory(), SolutionFactory()
        article1, article2, article3 = ArticleFactory(), ArticleFactory(), ArticleFactory()
        #
        solution1.links.clear()
        solution2.links.clear()
        solution3.links.clear()
        article1.links.clear()
        article2.links.clear()
        article3.links.clear()
        #
        solution1.links.add(self.weblink)
        solution2.links.add(self.weblink)
        solution3.links.add(self.weblink)
        article1.links.add(self.weblink)
        article2.links.add(self.weblink)
        article3.links.add(self.weblink)
        self.assertCountEqual(self.weblink.where_used(), (solution1, solution2, solution3, article1, article2, article3))
        #
        solution2.links.remove(self.weblink)
        article2.links.remove(self.weblink)
        article3.links.remove(self.weblink)
        self.assertCountEqual(self.weblink.where_used(), (solution1, solution3, article1))
        #
        solution1.links.remove(self.weblink)
        article3.links.add(self.weblink)
        article1.links.remove(self.weblink)
        self.assertCountEqual(self.weblink.where_used(), (solution3, article3))
