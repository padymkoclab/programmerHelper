
import unittest

from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from mylabour.utils import has_connect_to_internet

from apps.articles.factories import ArticleFactory
from apps.articles.models import Article


class ArticleManagerTest(TestCase):
    """
    Tests for ArticleManager.
    """

    @classmethod
    def setUpTestData(self):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def test_publish_articles_if_yet_not(self):
        # create new draft article
        article = ArticleFactory(status=Article.STATUS_ARTICLE.draft)
        self.assertEqual(article.status, Article.STATUS_ARTICLE.draft)
        # publish article
        Article.objects.publish_articles_if_yet_not(article)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.STATUS_ARTICLE.published)
        # attempt again publish article
        Article.objects.publish_articles_if_yet_not(article)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.STATUS_ARTICLE.published)

    def test_made_articles_as_draft_if_yet_not(self):
        # create new article and published it
        article = ArticleFactory(status=Article.STATUS_ARTICLE.published)
        self.assertEqual(article.status, Article.STATUS_ARTICLE.published)
        # made published article as draft
        Article.objects.made_articles_as_draft_if_yet_not(article)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.STATUS_ARTICLE.draft)
        # attermpt again made article as draft
        Article.objects.made_articles_as_draft_if_yet_not(article)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.STATUS_ARTICLE.draft)

    @unittest.skipIf(has_connect_to_internet() is False, 'Problem with connect to internet.')
    def test_check_exists_external_resourses_in_non_own_articles(self):
        # 1 article with valid link in 'source'
        ArticleFactory(source='http://google.com')
        self.assertTrue(Article.objects.check_exists_external_resourses_in_non_own_articles())

        # 2 article with valid link in 'source'
        ArticleFactory(source='http://yandex.ua')
        self.assertTrue(Article.objects.check_exists_external_resourses_in_non_own_articles())

        # 2 article with valid link in 'source' and 1 with broken
        article_with_broken_source_link_1 = ArticleFactory(source='http://broken_links_and_fuzzy_text.com')
        returned = Article.objects.check_exists_external_resourses_in_non_own_articles()
        self.assertFalse(returned[0])
        self.assertSequenceEqual(returned[1], [article_with_broken_source_link_1])

        # 2 article with valid link in 'source' and 2 with broken
        article_with_broken_source_link_2 = ArticleFactory(source='http://fuzzy_text_in_text.com')
        self.assertFalse(returned[0])
        self.assertSequenceEqual(returned[1], [article_with_broken_source_link_1, article_with_broken_source_link_2])

        # 2 article with valid link in 'source' and 3 with broken
        article_with_broken_source_link_3 = ArticleFactory(source='http://broken_links.com/unexistent_page_about_nothing/')
        self.assertFalse(returned[0])
        self.assertSequenceEqual(
            returned[1],
            [article_with_broken_source_link_1, article_with_broken_source_link_2, article_with_broken_source_link_3]
        )
