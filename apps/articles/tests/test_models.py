
from django.utils import timezone
from django.utils.text import slugify
from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.accounts.models import Account
from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.scopes.factories import ScopeFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink

from apps.articles.factories import ArticleFactory, ArticleSubsectionFactory, articles_factory
from apps.articles.models import Article


class ArticleTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        self.article = ArticleFactory()

    def test_create_article(self):
        account = Account.objects.random_accounts(1)
        data = dict(
            title='Кому и зачем потребовалась комната чёрной материи.',
            quotation='Страха не должно быть ни перед чем!',
            header="""
The table is a great way to show information about various prices for its products or services, especially,
some hosting company, they need to present the price of each plan clearly on table to easy
for users to looking. Those table should content text and features description easy users reading
information of each level has to offer in a table format. Depending on the contents,
the tables can be good for organizing many other types of data for deep clarity other than price.
""",
            conclusion="""
Today we’ll take a look to select some of beautiful css css3 tables.
These come from a variety of different sites.
If you’re interested in learning how to do this yourself, do not forget to take a look at some of our CSS3 tutorials!
I love css table design with shadows, rounded corners, gradients and all the CSS3 features.
That’s why, there are some days when I find myself designing in CSS3 more than in Photoshop.
The idea of building a features table just by using CSS/CSS3 came to me a while ago and
I decided to share it with you in this article.
""",
            picture='http://levashov.com/foto111.jpeg',
            status=Article.STATUS_ARTICLE.published,
            account=account,
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
        # adding comments
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
        article = ArticleFactory()
        new_account = Account.objects.exclude(pk=article.account.pk).random_accounts(1)
        data = dict(
            title='Why Python does not have operator CASE-SWITCH.',
            quotation='Важно чтобы было что показать.',
            header="""
Getting the message across – in style. That’s what typography is all about.
It greatly affects the mood of the reader. Like when you’re reading a manuscript,
most of the time, its on a yellow (ocher)-ish background.
When you’re reading stuff related to food, you’re going to find a lot of red color use.
That’s because the color read triggers the brain cells that relate to food.
For example, Burger King, KFC,McDonald’s – they all have the color red in common.
""",
            conclusion="""
In today’s article, I’m going to cover some really cool
typography effects you can use in your projects – or just play around with them!
I’ll be sharing the CSS code – so just paste them in your stylesheet and you’re good to go!
""",
            picture='http://python.org/foto211.jpeg',
            status=Article.STATUS_ARTICLE.draft,
            account=new_account,
            source='http://pydanny.com/django/why_python_does_not_have_operator_case_switch.html',
        )
        article.title = data['title']
        article.quotation = data['quotation']
        article.header = data['header']
        article.conclusion = data['conclusion']
        article.picture = data['picture']
        article.status = data['status']
        article.account = data['account']
        article.source = data['source']
        article.full_clean()
        article.save()
        self.assertEqual(article.title, data['title'])
        self.assertEqual(article.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(article.quotation, data['quotation'])
        self.assertEqual(article.header, data['header'])
        self.assertEqual(article.conclusion, data['conclusion'])
        self.assertEqual(article.picture, data['picture'])
        self.assertEqual(article.status, data['status'])
        self.assertEqual(article.account, data['account'])
        self.assertEqual(article.source, data['source'])

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

    def test_get_rating(self):
        self.article.scopes.clear()
        self.assertEqual(self.article.get_rating(), 0)
        ScopeFactory(content_object=self.article, scope=2)
        ScopeFactory(content_object=self.article, scope=1)
        ScopeFactory(content_object=self.article, scope=0)
        ScopeFactory(content_object=self.article, scope=4)
        ScopeFactory(content_object=self.article, scope=5)
        ScopeFactory(content_object=self.article, scope=1)
        ScopeFactory(content_object=self.article, scope=4)
        self.assertEqual(self.article.get_rating(), 2.1426)

    def test_get_volume(self):
        all_items = list()
        # length header and conclusion
        len_header = len(self.article.header)
        len_conclusion = len(self.article.conclusion)
        # add lengths
        all_items.extend([len_header, len_conclusion])
        for subsection in self.article.subsections.iterator():
            len_content = len(subsection.content)
            all_items.append(len_content)
        self.assertEqual(self.article.get_volume(), sum(all_items))
        # checkup with without subsections
        self.article.subsections.clear()
        self.assertEqual(self.article.get_volume(), len_header + len_conclusion)

    def test_tags_restrict(self):
        pass

    def test_links_restrict(self):
        pass


# class WritterTest(TestCase):
#     """

#     """

#     @classmethod
#     def setUpTestData(cls):
#         tags_factory(15)
#         web_links_factory(15)
#         badges_factory()
#         accounts_factory(15)
#         articles_factory(10)

#     def setUp(self):
#         self.writter = WritterFactory()

#     def test_create_writter(self):
#         data = dict(
#             title='Николай Левашов',
#             about="""
# с частицей "бы" и без нее, в начале придаточного предложения с
# инфинитивом. Вместо того, чтобы (разг.). Чем на мост нам итти, поищем
# лучше
# броду. Крылов. Чем кумушек считать трудиться, не лучше ль на себя, кума,
# оборотиться. Крылов. Чем бы помочь, он еще мешает.
#   3. В сочетании с сравн.
# """,
#             birthyear=1960,
#             deathyear=2012,
#         )
#         writter = Writter(**data)
#         writter.full_clean()
#         writter.save()
#         self.assertEqual(writter.title, data['title'])
#         self.assertEqual(writter.slug, slugify(data['title'], allow_unicode=True))
#         self.assertEqual(writter.about, data['about'])
#         self.assertEqual(writter.birthyear, data['birthyear'])
#         self.assertEqual(writter.deathyear, data['deathyear'])

#     def test_update_writter(self):
#         data = dict(
#             title='Валерий Дёмин',
#             about="""
#   1. После сравн. ст. и слов со знач. сравн. ст. присоединяет тот
# член предложения, с к-рым сравнивается что-н. лучше поздно, Чем никогда.
# Пословица.
#   2. с частицей "бы" и без нее, в начале придаточного предложения с
# инфинитивом. Вместо того, чтобы (разг.). Чем на мост нам итти, поищем
# лучше
# броду. Крылов. Чем кумушек считать трудиться, не лучше ль на себя, кума,
# оборотиться. Крылов. Чем бы помочь, он еще мешает.
#   3. В сочетании с сравн.
# ст. и при союзе "тем" в другом предложении употр. в знач. в какой
# степени,
# насколько. Чем дальше, тем лучше. Чем больше он говорил, тем больше
# краснел.
# """,
#             birthyear=1950,
#             deathyear=2016,
#         )
#         self.writter.title = data['title']
#         self.writter.about = data['about']
#         self.writter.birthyear = data['birthyear']
#         self.writter.deathyear = data['deathyear']
#         self.writter.full_clean()
#         self.writter.save()
#         self.assertEqual(self.writter.title, data['title'])
#         self.assertEqual(self.writter.slug, slugify(data['title'], allow_unicode=True))
#         self.assertEqual(self.writter.about, data['about'])
#         self.assertEqual(self.writter.birthyear, data['birthyear'])
#         self.assertEqual(self.writter.deathyear, data['deathyear'])

#     def test_delete_writter(self):
#         self.writter.delete()

#     def test_unique_slug(self):
#         same_title = 'русский Омар Хайам'
#         same_title_as_lower = same_title.lower()
#         same_title_as_upper = same_title.upper()
#         same_title_as_title = same_title.title()
#         slug_same_title = slugify(same_title, allow_unicode=True)
#         #
#         writter1 = WritterFactory()
#         writter2 = WritterFactory()
#         writter3 = WritterFactory()
#         #
#         writter1.title = same_title_as_lower
#         writter2.title = same_title_as_upper
#         writter3.title = same_title_as_title
#         #
#         writter1.full_clean()
#         writter2.full_clean()
#         writter3.full_clean()
#         #
#         writter1.save()
#         writter2.save()
#         writter3.save()
#         #
#         self.assertEqual(writter1.title, same_title_as_lower)
#         self.assertEqual(writter1.slug, slug_same_title)
#         self.assertEqual(writter2.title, same_title_as_upper)
#         self.assertEqual(writter2.slug, slug_same_title + '-2')
#         self.assertEqual(writter3.title, same_title_as_title)
#         self.assertEqual(writter3.slug, slug_same_title + '-3')

#     def test_get_absolute_url(self):
#         response = self.client.get(self.writter.get_absolute_url())
#         self.assertEqual(response.status_code, 200)

#     def test_if_birthyear_is_in_future(self):
#         self.writter.birthyear = NOW_YEAR + 1
#         self.assertRaisesMessage(ValidationError, 'Year of birth can not in future.', self.writter.full_clean)

#     def test_if_deathyear_is_in_future(self):
#         self.writter.deathyear = NOW_YEAR + 1
#         self.assertRaisesMessage(ValidationError, 'Year of death can not in future.', self.writter.full_clean)

#     def test_if_deathyear_is_more_or_equal_birthyear(self):
#         self.writter.deathyear = 1990
#         self.writter.birthyear = 2015
#         self.assertRaisesMessage(
#             ValidationError, 'Year of birth can not more or equal year of dearth.', self.writter.full_clean
#         )
#         self.writter.deathyear = 2014
#         self.writter.birthyear = 2014
#         self.assertRaisesMessage(
#             ValidationError, 'Year of birth can not more or equal year of dearth.', self.writter.full_clean
#         )

#     def test_if_small_range_beetween_deathyear_and_birthyear(self):
#         self.writter.birthyear = 1990
#         self.writter.deathyear = 1999
#         self.assertRaisesMessage(
#             ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
#         )
#         self.writter.birthyear = 1990
#         self.writter.deathyear = 2008
#         self.assertRaisesMessage(
#             ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
#         )
#         self.writter.birthyear = 1991
#         self.writter.deathyear = 2010
#         self.assertRaisesMessage(
#             ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
#         )
#         self.writter.birthyear = 1960
#         self.writter.deathyear = 1980
#         self.writter.full_clean()

#     def test_if_big_range_beetween_deathyear_and_birthyear(self):
#         self.writter.birthyear = 1800
#         self.writter.deathyear = 2000
#         self.assertRaisesMessage(
#             ValidationError, 'Very big range between year of birth and year of death.', self.writter.full_clean
#         )
#         self.writter.birthyear = 1860
#         self.writter.deathyear = 2015
#         self.assertRaisesMessage(
#             ValidationError, 'Very big range between year of birth and year of death.', self.writter.full_clean
#         )
#         self.writter.birthyear = 1830
#         self.writter.deathyear = 2005
#         self.assertRaisesMessage(
#             ValidationError, 'Very big range between year of birth and year of death.', self.writter.full_clean
#         )
#         self.writter.birthyear = 1850
#         self.writter.deathyear = 2000
#         self.writter.full_clean()

#     def test_if_very_young_writter(self):
#         self.writter.deathyear = None
#         #
#         self.writter.birthyear = NOW_YEAR
#         self.assertRaisesMessage(ValidationError, 'Writter not possible born so early.', self.writter.full_clean)
#         self.writter.birthyear = NOW_YEAR - 5
#         self.assertRaisesMessage(ValidationError, 'Writter not possible born so early.', self.writter.full_clean)
#         self.writter.birthyear = NOW_YEAR - 15
#         self.assertRaisesMessage(ValidationError, 'Writter not possible born so early.', self.writter.full_clean)
#         self.writter.birthyear = NOW_YEAR - 20
#         self.writter.full_clean()
