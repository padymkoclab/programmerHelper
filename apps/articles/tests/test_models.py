
from django.utils.text import slugify
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import accounts_factory, AccountFactory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.scopes.factories import ScopeFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.utils import generate_text_by_min_length, generate_text_certain_length

from apps.articles.factories import ArticleFactory, ArticleSubsectionFactory
from apps.articles.models import Article, ArticleSubsection


class ArticleTest(TestCase):
    """
    Tests for articles.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        self.article = ArticleFactory()
        self.article.full_clean()

    def test_create_article(self):
        data = dict(
            title='Кому и зачем потребовалась комната чёрной материи.',
            quotation='Страха не должно быть ни перед чем!',
            header=generate_text_by_min_length(100, as_p=True),
            conclusion=generate_text_by_min_length(100, as_p=True),
            picture='http://levashov.com/foto111.jpeg',
            status=Article.STATUS_ARTICLE.published,
            account=Account.objects.random_accounts(1),
            source='http://levashov.com/komy_boitsia_net_smerti_ratibor.html',
        )
        article = Article(**data)
        article.full_clean()
        article.save()
        # adding tags and links
        article.tags.add(*Tag.objects.random_tags(4))
        article.links.add(*WebLink.objects.random_weblinks(3))
        # adding subsections
        ArticleSubsectionFactory(article=article)
        ArticleSubsectionFactory(article=article)
        ArticleSubsectionFactory(article=article)
        ArticleSubsectionFactory(article=article)
        ArticleSubsectionFactory(article=article)
        # adding comments
        for i in range(8):
            CommentFactory(content_object=article)
        # adding scopes
        for i in range(10):
            ScopeFactory(content_object=article)
        #
        self.assertEqual(article.title, data['title'])
        self.assertEqual(article.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(article.header, data['header'])
        self.assertEqual(article.conclusion, data['conclusion'])
        self.assertEqual(article.picture, data['picture'])
        self.assertEqual(article.status, data['status'])
        self.assertEqual(article.quotation, data['quotation'])
        self.assertEqual(article.source, data['source'])
        self.assertEqual(article.account, data['account'])
        self.assertEqual(article.scopes.count(), 10)
        self.assertEqual(article.subsections.count(), 5)
        self.assertEqual(article.tags.count(), 4)
        self.assertEqual(article.links.count(), 3)
        self.assertEqual(article.comments.count(), 8)

    def test_update_article(self):
        new_account = AccountFactory()
        data = dict(
            title='Why Python does not have operator CASE-SWITCH.',
            quotation='Важно чтобы было что показать.',
            header=generate_text_by_min_length(100, as_p=True),
            conclusion=generate_text_by_min_length(100, as_p=True),
            picture='http://python.org/foto211.jpeg',
            status=Article.STATUS_ARTICLE.draft,
            account=new_account,
            source='http://pydanny.com/django/why_python_does_not_have_operator_case_switch.html',
        )
        self.article.title = data['title']
        self.article.quotation = data['quotation']
        self.article.header = data['header']
        self.article.conclusion = data['conclusion']
        self.article.picture = data['picture']
        self.article.status = data['status']
        self.article.account = data['account']
        self.article.source = data['source']
        self.article.full_clean()
        self.article.save()
        self.assertEqual(self.article.title, data['title'])
        self.assertEqual(self.article.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(self.article.quotation, data['quotation'])
        self.assertEqual(self.article.header, data['header'])
        self.assertEqual(self.article.conclusion, data['conclusion'])
        self.assertEqual(self.article.picture, data['picture'])
        self.assertEqual(self.article.status, data['status'])
        self.assertEqual(self.article.account, data['account'])
        self.assertEqual(self.article.source, data['source'])

    def test_delete_article(self):
        self.article.delete()

    def test_unique_slug(self):
        same_title = 'Использование Python для Web. Сравненительный анализ и смелые выводы.'
        same_title_as_lower = same_title.lower()
        same_title_as_upper = same_title.upper()
        same_title_as_title = same_title.title()
        slug_same_title = slugify(same_title, allow_unicode=True)
        account = Account.objects.random_accounts(1)
        new_account = Account.objects.exclude(pk=account.pk).random_accounts(1)
        #
        article11 = ArticleFactory(title=same_title_as_lower, account=account)
        article12 = ArticleFactory(title=same_title_as_upper, account=account)
        article13 = ArticleFactory(title=same_title_as_title, account=account)
        article21 = ArticleFactory(title=same_title_as_lower, account=new_account)
        article22 = ArticleFactory(title=same_title_as_upper, account=new_account)
        article23 = ArticleFactory(title=same_title_as_title, account=new_account)
        #
        self.assertEqual(article11.title, same_title_as_lower)
        self.assertEqual(article11.slug, slug_same_title)
        self.assertEqual(article12.title, same_title_as_upper)
        self.assertEqual(article12.slug, slug_same_title + '-2')
        self.assertEqual(article13.title, same_title_as_title)
        self.assertEqual(article13.slug, slug_same_title + '-3')
        self.assertEqual(article21.title, same_title_as_lower)
        self.assertEqual(article21.slug, slug_same_title)
        self.assertEqual(article22.title, same_title_as_upper)
        self.assertEqual(article22.slug, slug_same_title + '-2')
        self.assertEqual(article23.title, same_title_as_title)
        self.assertEqual(article23.slug, slug_same_title + '-3')

    def test_get_absolute_url(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_admin_page_url(self):
        raise NotImplementedError

    def test_get_rating(self):
        self.article.scopes.clear()
        self.assertEqual(self.article.get_rating(), .0)
        ScopeFactory(content_object=self.article, scope=2)
        ScopeFactory(content_object=self.article, scope=1)
        ScopeFactory(content_object=self.article, scope=0)
        ScopeFactory(content_object=self.article, scope=4)
        ScopeFactory(content_object=self.article, scope=5)
        ScopeFactory(content_object=self.article, scope=1)
        ScopeFactory(content_object=self.article, scope=4)
        self.assertEqual(self.article.get_rating(), 2.4286)

    def test_get_volume(self):

        # length header and conclusion
        self.article.header = generate_text_certain_length(300)
        self.article.conclusion = generate_text_certain_length(541)
        self.article.full_clean()
        self.article.save()

        # clear and a anew adding the subsections
        ArticleSubsectionFactory(article=self.article, content=generate_text_certain_length(300))
        ArticleSubsectionFactory(article=self.article, content=generate_text_certain_length(258))
        ArticleSubsectionFactory(article=self.article, content=generate_text_certain_length(941))
        self.assertEqual(self.article.get_volume(), 2340)

        # checkup with without subsections
        self.article.subsections.filter().delete()
        self.assertEqual(self.article.get_volume(), 841)

    def test_related_articles(self):
        raise NotImplementedError


class ArticleSubsectionTest(TestCase):
    """
    Tests for subsections of articles.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        self.article = ArticleFactory()
        self.article.full_clean()
        self.subsection = ArticleSubsectionFactory(article=self.article)
        self.subsection.full_clean()

    def test_create_subsection(self):
        data = dict(
            title='How to white obfusted python.',
            content=generate_text_by_min_length(1000, as_p=True),
            article=self.article,
        )
        subsection = ArticleSubsection(**data)
        subsection.full_clean()
        subsection.save()
        self.assertEqual(subsection.title, data['title'])
        self.assertEqual(subsection.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(subsection.article, data['article'])
        self.assertEqual(subsection.content, data['content'])

    def test_update_subsection(self):
        data = dict(
            title='I never Meta model I didn`t like.',
            content=generate_text_by_min_length(1000, as_p=True),
            article=self.article,
        )
        #
        self.subsection.title = data['title']
        self.subsection.article = data['article']
        self.subsection.content = data['content']
        self.subsection.full_clean()
        self.subsection.save()
        #
        self.assertEqual(self.subsection.title, data['title'])
        self.assertEqual(self.subsection.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(self.subsection.article, data['article'])
        self.assertEqual(self.subsection.content, data['content'])

    def test_delete_subsection(self):
        self.subsection.delete()

    def test_unique_slug(self):
        same_title = 'All grammer of English for nineteen minutes and thirty-sever seconds, in other words - quickly.'
        same_title_as_lower = same_title.lower()
        same_title_as_upper = same_title.upper()
        same_title_as_title = same_title.title()
        article1 = ArticleFactory()
        article2 = ArticleFactory()
        slug_same_title = slugify(same_title, allow_unicode=True)
        #
        subsection11 = ArticleSubsectionFactory(article=article1, title=same_title_as_lower)
        subsection12 = ArticleSubsectionFactory(article=article1, title=same_title_as_upper)
        subsection13 = ArticleSubsectionFactory(article=article1, title=same_title_as_title)
        subsection21 = ArticleSubsectionFactory(article=article2, title=same_title_as_lower)
        subsection22 = ArticleSubsectionFactory(article=article2, title=same_title_as_upper)
        subsection23 = ArticleSubsectionFactory(article=article2, title=same_title_as_title)
        #
        self.assertEqual(subsection11.title, same_title_as_lower)
        self.assertEqual(subsection11.slug, slug_same_title)
        self.assertEqual(subsection12.title, same_title_as_upper)
        self.assertEqual(subsection12.slug, slug_same_title + '-2')
        self.assertEqual(subsection13.title, same_title_as_title)
        self.assertEqual(subsection13.slug, slug_same_title + '-3')
        self.assertEqual(subsection21.title, same_title_as_lower)
        self.assertEqual(subsection21.slug, slug_same_title)
        self.assertEqual(subsection22.title, same_title_as_upper)
        self.assertEqual(subsection22.slug, slug_same_title + '-2')
        self.assertEqual(subsection23.title, same_title_as_title)
        self.assertEqual(subsection23.slug, slug_same_title + '-3')
