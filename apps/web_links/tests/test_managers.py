
from django.test import TestCase

from apps.solutions.factories import solutions_factory
from apps.solutions.models import Solution
from apps.articles.factories import articles_factory
from apps.articles.models import Article
from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory

from apps.web_links.models import WebLink


class WebLinkManagerTest(TestCase):
    """
    Tests for manager of model of web links.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(20)
        badges_factory()
        accounts_factory(15)
        solutions_factory(15)
        articles_factory(15)

    def setUp(self):
        assert Solution.objects.count() == 15, 'Test supposes strict 15 a solutions.'
        assert Article.objects.count() == 15, 'Test supposes strict 15 a articles.'
        #
        for solution in Solution.objects.iterator():
            solution.links.clear()
        for article in Article.objects.iterator():
            article.links.clear()

    def test_get_total_count_usage_weblinks_in_solutions(self):
        self.assertEqual(WebLink.objects.get_total_count_usage_weblinks_in_solutions(), 0)
        #
        for solution, count_weblinks in zip(
            Solution.objects.iterator(),
            [1, 3, 6, 7, 9, 9, 0, 1, 7, 15, 12, 6, 0, 4]
        ):
            if count_weblinks != 0:
                if count_weblinks == 1:
                    weblinks = [WebLink.objects.random_weblinks(count_weblinks)]
                else:
                    weblinks = WebLink.objects.random_weblinks(count_weblinks)
                solution.links.set(weblinks)
        self.assertEqual(WebLink.objects.get_total_count_usage_weblinks_in_solutions(), 80)

    def test_get_total_count_usage_weblinks_in_articles(self):
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_solutions'], 0)
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_articles'], 0)
        #
        for article, count_weblinks in zip(
            Article.objects.iterator(),
            [4, 2, 0, 9, 10, 14, 7, 8, 12, 0, 3, 1, 6, 11, 9]
        ):
            if count_weblinks != 0:
                if count_weblinks == 1:
                    weblinks = [WebLink.objects.random_weblinks(count_weblinks)]
                else:
                    weblinks = WebLink.objects.random_weblinks(count_weblinks)
                article.links.set(weblinks)
        self.assertEqual(WebLink.objects.get_total_count_usage_weblinks_in_articles(), 96)

    def test_get_statistics_usage_web_links(self):
        self.assertEqual(WebLink.objects.get_total_count_usage_weblinks_in_articles(), 0)
        #
        for solution, count_weblinks in zip(
            Solution.objects.iterator(),
            [0, 12, 10, 12, 8, 13, 5, 9, 12, 3, 6, 14, 7, 0, 3]
        ):
            if count_weblinks != 0:
                if count_weblinks == 1:
                    weblinks = [WebLink.objects.random_weblinks(count_weblinks)]
                else:
                    weblinks = WebLink.objects.random_weblinks(count_weblinks)
                solution.links.set(weblinks)
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_solutions'], 114)
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_articles'], 0)
        #
        for article, count_weblinks in zip(
            Article.objects.iterator(),
            [0, 14, 12, 3, 9, 11, 5, 11, 5, 3, 13, 0, 3, 5, 14]
        ):
            if count_weblinks != 0:
                if count_weblinks == 1:
                    weblinks = [WebLink.objects.random_weblinks(count_weblinks)]
                else:
                    weblinks = WebLink.objects.random_weblinks(count_weblinks)
                article.links.set(weblinks)
        #
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_solutions'], 114)
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_articles'], 108)
        #
        for solution in Solution.objects.iterator():
            solution.links.clear()
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_solutions'], 0)
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_articles'], 108)
        #
        for article in Article.objects.iterator():
            article.links.clear()
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_solutions'], 0)
        self.assertEqual(WebLink.objects.get_statistics_usage_web_links()['count_usage_in_articles'], 0)
