
from django.utils import timezone
from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.scopes.factories import ScopeFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.utils import generate_text_certain_length

from apps.articles.factories import articles_factory, ArticleSubsectionFactory
from apps.articles.models import Article


class ArticleQuerySetTest(TestCase):
    """

    """

    @classmethod
    def setUpTestData(self):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15, True)

    def setUp(self):
        articles_factory(10)

    def test_articles_with_rating(self):
        article1, article2, article3, article4 = Article.objects.all()[:4]
        article1.scopes.clear()
        article2.scopes.clear()
        article3.scopes.clear()
        article4.scopes.clear()
        #
        ScopeFactory(content_object=article1, scope=2)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article1, scope=5)
        ScopeFactory(content_object=article1, scope=4)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=2)
        #
        ScopeFactory(content_object=article2, scope=1)
        ScopeFactory(content_object=article2, scope=4)
        ScopeFactory(content_object=article2, scope=2)
        #
        ScopeFactory(content_object=article3, scope=1)
        #
        articles_with_rating = Article.objects.articles_with_rating()
        self.assertEqual(articles_with_rating.get(pk=article1.pk).rating, 2.8571)
        self.assertEqual(articles_with_rating.get(pk=article2.pk).rating, 2.3333)
        self.assertEqual(articles_with_rating.get(pk=article3.pk).rating, 1)
        self.assertEqual(articles_with_rating.get(pk=article4.pk).rating, .0)

    def test_articles_with_volume(self):
        article1, article2, article3 = Article.objects.all()[:3]
        article1.subsections.filter().delete()
        article2.subsections.filter().delete()
        article3.subsections.filter().delete()
        #
        article1.header = generate_text_certain_length(645)
        ArticleSubsectionFactory(article=article1, number=1, title='Virtualenv', content=generate_text_certain_length(841))
        ArticleSubsectionFactory(article=article1, number=2, title='Virtualwrapper', content=generate_text_certain_length(751))
        article1.conclusion = generate_text_certain_length(554)
        article1.full_clean()
        article1.save()
        #
        article2.header = generate_text_certain_length(389)
        ArticleSubsectionFactory(article=article2, number=1, title='Vagrant', content=generate_text_certain_length(789))
        article2.conclusion = generate_text_certain_length(287)
        article2.full_clean()
        article2.save()
        #
        article3.header = generate_text_certain_length(897)
        article3.conclusion = generate_text_certain_length(714)
        article3.full_clean()
        article3.save()
        #
        articles_with_volume = Article.objects.articles_with_volume()
        self.assertEqual(articles_with_volume.get(pk=article1.pk).volume, 2791)
        self.assertEqual(articles_with_volume.get(pk=article2.pk).volume, 1465)
        self.assertEqual(articles_with_volume.get(pk=article3.pk).volume, 1611)

    def test_articles_with_count_comments(self):
        for article in Article.objects.iterator():
            article.comments.clear()
        article1, article2, article3, article4 = Article.objects.all()[:4]
        #
        CommentFactory(content_object=article1)
        CommentFactory(content_object=article1)
        CommentFactory(content_object=article1)
        #
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        CommentFactory(content_object=article2)
        #
        CommentFactory(content_object=article3)
        #
        articles_with_count_comments = Article.objects.articles_with_count_comments()
        self.assertEqual(articles_with_count_comments.get(pk=article1.pk).count_comments, 3)
        self.assertEqual(articles_with_count_comments.get(pk=article2.pk).count_comments, 11)
        self.assertEqual(articles_with_count_comments.get(pk=article3.pk).count_comments, 1)
        self.assertEqual(articles_with_count_comments.get(pk=article4.pk).count_comments, 0)

    def test_articles_with_count_tags(self):
        article1, article2, article3, article4 = Article.objects.all()[:4]
        #
        article1.tags.set(Tag.objects.random_tags(5))
        article2.tags.set(Tag.objects.random_tags(4))
        article3.tags.set([Tag.objects.random_tags(1)])
        article4.tags.clear()
        #
        articles_with_count_tags = Article.objects.articles_with_count_tags()
        self.assertEqual(articles_with_count_tags.get(pk=article1.pk).count_tags, 5)
        self.assertEqual(articles_with_count_tags.get(pk=article2.pk).count_tags, 4)
        self.assertEqual(articles_with_count_tags.get(pk=article3.pk).count_tags, 1)
        self.assertEqual(articles_with_count_tags.get(pk=article4.pk).count_tags, 0)

    def test_articles_with_count_scopes(self):
        article1, article2, article3, article4 = Article.objects.all()[:4]
        article1.scopes.clear()
        article2.scopes.clear()
        article3.scopes.clear()
        article4.scopes.clear()
        #
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article2, scope=1)
        ScopeFactory(content_object=article2, scope=1)
        ScopeFactory(content_object=article3, scope=1)
        ScopeFactory(content_object=article3, scope=1)
        ScopeFactory(content_object=article3, scope=1)
        ScopeFactory(content_object=article3, scope=1)
        ScopeFactory(content_object=article3, scope=1)
        #
        articles_with_count_scopes = Article.objects.articles_with_count_scopes()
        self.assertEqual(articles_with_count_scopes.get(pk=article1.pk).count_scopes, 3)
        self.assertEqual(articles_with_count_scopes.get(pk=article2.pk).count_scopes, 2)
        self.assertEqual(articles_with_count_scopes.get(pk=article3.pk).count_scopes, 5)
        self.assertEqual(articles_with_count_scopes.get(pk=article4.pk).count_scopes, 0)

    def test_articles_with_count_links(self):
        article1, article2, article3, article4 = Article.objects.all()[:4]
        #
        article1.links.set(WebLink.objects.random_weblinks(4))
        article2.links.set([WebLink.objects.random_weblinks(1)])
        article3.links.set(WebLink.objects.random_weblinks(5))
        article4.links.clear()
        #
        articles_with_count_links = Article.objects.articles_with_count_links()
        self.assertEqual(articles_with_count_links.get(pk=article1.pk).count_links, 4)
        self.assertEqual(articles_with_count_links.get(pk=article2.pk).count_links, 1)
        self.assertEqual(articles_with_count_links.get(pk=article3.pk).count_links, 5)
        self.assertEqual(articles_with_count_links.get(pk=article4.pk).count_links, 0)

    def test_articles_with_count_subsections(self):
        article1, article2, article3, article4 = Article.objects.all()[:4]
        article1.subsections.filter().delete()
        article2.subsections.filter().delete()
        article3.subsections.filter().delete()
        article4.subsections.filter().delete()
        #
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article2)
        ArticleSubsectionFactory(article=article2)
        ArticleSubsectionFactory(article=article2)
        ArticleSubsectionFactory(article=article3)
        #
        articles_with_count_subsections = Article.objects.articles_with_count_subsections()
        self.assertEqual(articles_with_count_subsections.get(pk=article1.pk).count_subsections, 5)
        self.assertEqual(articles_with_count_subsections.get(pk=article2.pk).count_subsections, 3)
        self.assertEqual(articles_with_count_subsections.get(pk=article3.pk).count_subsections, 1)
        self.assertEqual(articles_with_count_subsections.get(pk=article4.pk).count_subsections, 0)

    def test_articles_with_rating_and_count_comments_subsections_tags_links_scopes(self):
        articles = Article.objects.all()[:4]
        for article in articles:
            article.subsections.filter().delete()
            article.comments.clear()
            article.scopes.clear()
            article.tags.clear()
            article.links.clear()
        article1, article2, article3, article4 = articles
        #
        article1.tags.set(Tag.objects.random_tags(5))
        article1.links.set(WebLink.objects.random_weblinks(5))
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        ArticleSubsectionFactory(article=article1)
        CommentFactory(content_object=article1)
        CommentFactory(content_object=article1)
        CommentFactory(content_object=article1)
        CommentFactory(content_object=article1)
        CommentFactory(content_object=article1)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=4)
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article1, scope=2)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=4)
        ScopeFactory(content_object=article1, scope=5)
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=2)
        ScopeFactory(content_object=article1, scope=1)
        #
        article2.tags.set([Tag.objects.random_tags(1)])
        article2.links.set([WebLink.objects.random_weblinks(1)])
        ArticleSubsectionFactory(article=article2)
        CommentFactory(content_object=article2)
        ScopeFactory(content_object=article2, scope=2)
        #
        article3.tags.set(Tag.objects.random_tags(2))
        article3.links.set(WebLink.objects.random_weblinks(4))
        ArticleSubsectionFactory(article=article3)
        ArticleSubsectionFactory(article=article3)
        ArticleSubsectionFactory(article=article3)
        CommentFactory(content_object=article3)
        CommentFactory(content_object=article3)
        CommentFactory(content_object=article3)
        CommentFactory(content_object=article3)
        ScopeFactory(content_object=article3, scope=1)
        ScopeFactory(content_object=article3, scope=4)
        ScopeFactory(content_object=article3, scope=2)
        ScopeFactory(content_object=article3, scope=2)
        ScopeFactory(content_object=article3, scope=1)
        ScopeFactory(content_object=article3, scope=3)
        ScopeFactory(content_object=article3, scope=4)
        ScopeFactory(content_object=article3, scope=2)
        #
        articles = Article.objects.articles_with_rating_and_count_comments_subsections_tags_links_scopes()
        self.assertEqual(articles.get(pk=article1.pk).rating, 2.5385)
        self.assertEqual(articles.get(pk=article1.pk).count_comments, 5)
        self.assertEqual(articles.get(pk=article1.pk).count_subsections, 5)
        self.assertEqual(articles.get(pk=article1.pk).count_scopes, 13)
        self.assertEqual(articles.get(pk=article1.pk).count_tags, 5)
        self.assertEqual(articles.get(pk=article1.pk).count_links, 5)
        self.assertEqual(articles.get(pk=article2.pk).rating, 2.0)
        self.assertEqual(articles.get(pk=article2.pk).count_comments, 1)
        self.assertEqual(articles.get(pk=article2.pk).count_subsections, 1)
        self.assertEqual(articles.get(pk=article2.pk).count_scopes, 1)
        self.assertEqual(articles.get(pk=article2.pk).count_tags, 1)
        self.assertEqual(articles.get(pk=article2.pk).count_links, 1)
        self.assertEqual(articles.get(pk=article3.pk).rating, 2.375)
        self.assertEqual(articles.get(pk=article3.pk).count_comments, 4)
        self.assertEqual(articles.get(pk=article3.pk).count_subsections, 3)
        self.assertEqual(articles.get(pk=article3.pk).count_scopes, 8)
        self.assertEqual(articles.get(pk=article3.pk).count_tags, 2)
        self.assertEqual(articles.get(pk=article3.pk).count_links, 4)
        self.assertEqual(articles.get(pk=article4.pk).rating, 0)
        self.assertEqual(articles.get(pk=article4.pk).count_comments, 0)
        self.assertEqual(articles.get(pk=article4.pk).count_subsections, 0)
        self.assertEqual(articles.get(pk=article4.pk).count_scopes, 0)
        self.assertEqual(articles.get(pk=article4.pk).count_tags, 0)
        self.assertEqual(articles.get(pk=article4.pk).count_links, 0)

    def test_published_articles(self):
        # all published articles
        Article.objects.update(status=Article.STATUS_ARTICLE.published)
        self.assertEqual(Article.objects.published_articles().count(), 10)
        # not published articles
        Article.objects.update(status=Article.STATUS_ARTICLE.draft)
        self.assertEqual(Article.objects.published_articles().count(), 0)
        # two articles are published, other - not
        first_article = Article.objects.first()
        first_article.status = Article.STATUS_ARTICLE.published
        first_article.full_clean()
        first_article.save()
        last_article = Article.objects.last()
        last_article.status = Article.STATUS_ARTICLE.published
        last_article.full_clean()
        last_article.save()
        self.assertEqual(Article.objects.published_articles().count(), 2)
        # reset
        Article.objects.update(status=Article.STATUS_ARTICLE.draft)
        # each second article is published
        pks = Article.objects.values_list('pk', flat=True)[::2]
        Article.objects.filter(pk__in=pks).update(status=Article.STATUS_ARTICLE.published)
        self.assertEqual(Article.objects.published_articles().count(), 5)

    def test_draft_articles(self):
        # all draft articles
        Article.objects.update(status=Article.STATUS_ARTICLE.draft)
        self.assertEqual(Article.objects.draft_articles().count(), 10)
        Article.objects.update(status=Article.STATUS_ARTICLE.published)
        # two articles are draft, other - not
        first_article = Article.objects.first()
        first_article.status = Article.STATUS_ARTICLE.draft
        first_article.full_clean()
        first_article.save()
        last_article = Article.objects.last()
        last_article.status = Article.STATUS_ARTICLE.draft
        last_article.full_clean()
        last_article.save()
        self.assertEqual(Article.objects.draft_articles().count(), 2)
        # not draft articles
        Article.objects.update(status=Article.STATUS_ARTICLE.published)
        self.assertEqual(Article.objects.draft_articles().count(), 0)
        # each second article is draft
        pks = Article.objects.values_list('pk', flat=True)[::2]
        Article.objects.filter(pk__in=pks).update(status=Article.STATUS_ARTICLE.draft)
        self.assertEqual(Article.objects.draft_articles().count(), 5)

    def test_weekly_articles(self):
        now = timezone.now()
        for article in Article.objects.iterator():
            article.date_added = now - timezone.timedelta(days=8)
            article.full_clean()
            article.save()
        self.assertEqual(Article.objects.weekly_articles().count(), 0)
        dates = [
            # satisfy dates
            now,
            now - timezone.timedelta(days=1),
            now - timezone.timedelta(days=2),
            now - timezone.timedelta(days=3),
            now - timezone.timedelta(days=4),
            now - timezone.timedelta(days=5),
            now - timezone.timedelta(days=6),
            now - timezone.timedelta(days=6, hours=23, minutes=59, seconds=59),
            # not satisfy dates
            now - timezone.timedelta(days=7),
            now - timezone.timedelta(days=8),
            now - timezone.timedelta(days=9),
        ]
        for date, article in zip(dates, Article.objects.all()):
            article.date_added = date
            article.full_clean()
            article.save()
        self.assertEqual(Article.objects.weekly_articles().count(), 8)

    def test_articles_from_external_resourse(self):
        # all articles is own of site
        Article.objects.update(source=None)
        self.assertEqual(Article.objects.articles_from_external_resourse().count(), 0)
        # two articles are external, other - not
        first_article = Article.objects.first()
        first_article.source = 'http://zabuto.js/simple_and_stupid_development.html'
        first_article.full_clean()
        first_article.save()
        last_article = Article.objects.last()
        last_article.source = 'http://tornado.com/best_web_server_for_python/'
        last_article.full_clean()
        last_article.save()
        self.assertEqual(Article.objects.articles_from_external_resourse().count(), 2)
        # all articles is external
        Article.objects.update(source='http://djangoproject.com/models')
        self.assertEqual(Article.objects.articles_from_external_resourse().count(), 10)
        # reset
        Article.objects.update(source=None)
        # each second article is external
        pks = Article.objects.values_list('pk', flat=True)[::2]
        Article.objects.filter(pk__in=pks).update(source='http://python.org/how_to_made')
        self.assertEqual(Article.objects.articles_from_external_resourse().count(), 5)

    def test_own_articles(self):
        # all articles is own of site
        Article.objects.update(source=None)
        self.assertEqual(Article.objects.own_articles().count(), 10)
        # two articles are external, other - not
        first_article = Article.objects.first()
        first_article.source = 'http://jquery.js/simple_and_stupid_development.html'
        first_article.full_clean()
        first_article.save()
        last_article = Article.objects.last()
        last_article.source = 'http://tornado.com/best_web_server_for_python/'
        last_article.full_clean()
        last_article.save()
        self.assertEqual(Article.objects.own_articles().count(), 8)
        # all articles is external
        Article.objects.update(source='http://djangoproject.com/models')
        self.assertEqual(Article.objects.own_articles().count(), 0)
        # reset
        Article.objects.update(source=None)
        # each second article is external
        pks = Article.objects.values_list('pk', flat=True)[::2]
        Article.objects.filter(pk__in=pks).update(source='http://python.org/how_to_made')
        self.assertEqual(Article.objects.own_articles().count(), 5)

    def test_hot_articles(self):
        """Test what each article with count comments 7 and more enters in categories "Hot" articles."""

        for article in Article.objects.iterator():
            article.comments.clear()
        self.assertEqual(Article.objects.hot_articles().count(), 0)
        for count_comments, article in enumerate(Article.objects.all()):
            for i in range(count_comments):
                CommentFactory(content_object=article)
        self.assertCountEqual(Article.objects.hot_articles(), Article.objects.all()[::-1][:3])

    def test_popular_articles(self):
        """Test what each article with rating 5 and more consider as popular."""

        for article in Article.objects.iterator():
            article.scopes.clear()
        self.assertEqual(Article.objects.popular_articles().count(), 0)
        article1, article2, article3, article4, article5 = Article.objects.all()[:5]
        # 4
        ScopeFactory(content_object=article1, scope=4)
        # 54 / 11
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=5)
        ScopeFactory(content_object=article2, scope=4)
        self.assertEqual(article2.get_rating(), 4.9091)
        # 5
        ScopeFactory(content_object=article3, scope=5)
        # 45 / 11
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=2)
        ScopeFactory(content_object=article4, scope=2)
        ScopeFactory(content_object=article4, scope=1)
        self.assertEqual(article4.get_rating(), 4.0909)
        #
        self.assertCountEqual(Article.objects.popular_articles(), [article1, article2, article3, article4])

    def test_validate_input_articles_by_rating(self):
        # if not nothing limitation
        self.assertRaisesMessage(
            AttributeError,
            'Please point at least either min_rating or max_rating.',
            Article.objects.articles_by_rating
        )
        # if max_rating is less than min_rating
        self.assertRaisesMessage(
            ValueError,
            'Don`t right values: min_rating is more than max_rating.',
            Article.objects.articles_by_rating,
            2,
            1
        )

    def test_articles_by_rating(self):

        for article in Article.objects.iterator():
            article.scopes.clear()
        article1, article2, article3, article4, article5, article6, article7 = Article.objects.all()[:7]
        Article.objects.exclude(pk__in=Article.objects.values('pk')[:7]).delete()
        # 3
        ScopeFactory(content_object=article1, scope=2)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=4)
        # 4.3333
        ScopeFactory(content_object=article2, scope=4)
        ScopeFactory(content_object=article2, scope=4)
        ScopeFactory(content_object=article2, scope=5)
        # 5
        ScopeFactory(content_object=article3, scope=5)
        ScopeFactory(content_object=article3, scope=5)
        ScopeFactory(content_object=article3, scope=5)
        # 3.6666
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=5)
        ScopeFactory(content_object=article4, scope=1)
        # 2.6667
        ScopeFactory(content_object=article5, scope=1)
        ScopeFactory(content_object=article5, scope=4)
        ScopeFactory(content_object=article5, scope=3)
        # 1.6667
        ScopeFactory(content_object=article6, scope=1)
        ScopeFactory(content_object=article6, scope=1)
        ScopeFactory(content_object=article6, scope=3)
        # 1
        ScopeFactory(content_object=article7, scope=1)
        ScopeFactory(content_object=article7, scope=1)
        ScopeFactory(content_object=article7, scope=1)
        # find by min rating
        self.assertCountEqual(
            Article.objects.articles_by_rating(min_rating=1),
            [article1, article2, article3, article4, article5, article6, article7]
        )
        self.assertCountEqual(
            Article.objects.articles_by_rating(min_rating=2),
            [article1, article2, article3, article4, article5],
        )
        self.assertCountEqual(Article.objects.articles_by_rating(min_rating=2.7), [article1, article2, article3, article4])
        self.assertCountEqual(Article.objects.articles_by_rating(min_rating=3.1), [article2, article3, article4])
        self.assertCountEqual(Article.objects.articles_by_rating(min_rating=3.9), [article2, article3])
        # find by max rating
        self.assertCountEqual(Article.objects.articles_by_rating(max_rating=1), [article7])
        self.assertCountEqual(Article.objects.articles_by_rating(max_rating=2), [article6, article7])
        self.assertCountEqual(Article.objects.articles_by_rating(max_rating=3.1), [article1, article5, article6, article7])
        self.assertCountEqual(
            Article.objects.articles_by_rating(max_rating=3.9),
            [article1, article4, article5, article6, article7]
        )
        self.assertCountEqual(
            Article.objects.articles_by_rating(max_rating=4.7),
            [article1, article2, article4, article5, article6, article7]
        )
        # find by min and max limitations of rating
        self.assertCountEqual(
            Article.objects.articles_by_rating(1, 3),
            [article1, article5, article6, article7]
        )
        self.assertCountEqual(
            Article.objects.articles_by_rating(2, 5),
            [article1, article2, article3, article4, article5],
        )
        self.assertCountEqual(Article.objects.articles_by_rating(2.7, 3.5), [article1])
        self.assertCountEqual(Article.objects.articles_by_rating(3.1, 4.8), [article2, article4])
        self.assertCountEqual(Article.objects.articles_by_rating(3.9, 5), [article2, article3])
        self.assertCountEqual(Article.objects.articles_by_rating(1.8, 1.9), [])

    def test_big_articles(self):
        for article in Article.objects.iterator():
            article.subsections.filter().delete()
            article.header = 'This is simple article about Python and JS.'
            article.conclusion = 'I decided what Python and JS is neccesary for each web-developer.'
            article.full_clean()
            article.save()
        article1, article2, article3, article4, article5 = Article.objects.all()[:5]
        self.assertEqual(Article.objects.big_articles().count(), 0)
        #
        article1.header = generate_text_certain_length(10000)
        article1.full_clean()
        article1.save()
        self.assertCountEqual(Article.objects.big_articles(), [article1])
        #
        article2.conclusion = generate_text_certain_length(10000)
        article2.full_clean()
        article2.save()
        self.assertCountEqual(Article.objects.big_articles(), [article1, article2])
        #
        ArticleSubsectionFactory(article=article3, content=generate_text_certain_length(10000))
        self.assertCountEqual(Article.objects.big_articles(), [article1, article2, article3])
        #
        ArticleSubsectionFactory(article=article4, content=generate_text_certain_length(3000))
        ArticleSubsectionFactory(article=article4, content=generate_text_certain_length(3000))
        ArticleSubsectionFactory(article=article4, content=generate_text_certain_length(4000))
        self.assertCountEqual(Article.objects.big_articles(), [article1, article2, article3, article4])
        #
        ArticleSubsectionFactory(article=article5, content=generate_text_certain_length(9000))
        self.assertCountEqual(Article.objects.big_articles(), [article1, article2, article3, article4])
