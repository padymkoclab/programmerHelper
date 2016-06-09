
from django.core.exceptions import ValidationError
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

from apps.articles.factories import ArticleFactory, ArticleSubsectionFactory
from apps.articles.models import Article, ArticleSubsection


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
        new_account = AccountFactory()
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
        self.article.subsections.filter().delete()
        self.assertEqual(self.article.get_volume(), len_header + len_conclusion)

    def test_tags_restrict(self):
        pass

    def test_links_restrict(self):
        pass


class ArticleSubsectionTest(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        self.article = ArticleFactory()
        self.subsection = ArticleSubsectionFactory(article=self.article)

    def test_create_subsection(self):
        data = dict(
            title='How to white obfusted python.',
            content="""
ɔbfʌskeɪt гл.; книж. 1) затемнять (тж. перен.) Syn : darken, obscure
2) а) озадачивать, сбивать с толку, ставить в тупик
б) загонять в угол в) затуманивать рассудок Syn : stupefy, bewilder
(книжное) путать, сбивать (с толку); туманить рассудок (американизм)
(умышленно) запутывать вопрос; напускать туман - to * a problem with
extraneous information осложнять задачу из-за несущественной информации
(специальное) затемнять, затенять obfuscate книжн. затемнять (свет,
вопрос и т. п.) ~ книжн. сбивать с толку; туманить рассудок
""",
            number=2,
            article=self.article,
        )
        subsection = ArticleSubsection(**data)
        subsection.full_clean()
        subsection.save()
        self.assertEqual(subsection.title, data['title'])
        self.assertEqual(subsection.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(subsection.article, data['article'])
        self.assertEqual(subsection.number, data['number'])
        self.assertEqual(subsection.content, data['content'])

    def test_update_subsection(self):
        data = dict(
            title='I never Meta model I didn`t like.',
            content="""
1) а) зрелый, спелый (о фрукте, злаке и т. п.) Syn : full-blown б) зрелый, выдержанный (о вине и т. п.)
Syn : ripe II в) созревший (о зародыше и т. п.), доношенный (о ребенке)
2) взрослый, возмужавший (о человеке) mature age/years ≈ зрелый возраст/зрелые годы mature wisdom
≈ приходящая с возрастом мудрость mature student ≈ взрослый студент (довольно взрослый
для обычного студенческого возраста) Syn : adult, ripe, full-grown, grown-up, of age
3) сложившийся, сформировавшийся (об экономической ситуации и т. п.), ставший прибыльным
(об отрасли чего-л., сфере деятельности и т. п.) show-business is a mature industry ≈ шоу-бизнес
- процветающий теперь вид производства 4) продуманный (о мнении, поступке и т. п.);
зрелый, разумный (о решении и т. п.)
""",
            number=3,
            article=self.article,
        )
        #
        self.subsection.title = data['title']
        self.subsection.article = data['article']
        self.subsection.number = data['number']
        self.subsection.content = data['content']
        self.subsection.full_clean()
        self.subsection.save()
        #
        self.assertEqual(self.subsection.title, data['title'])
        self.assertEqual(self.subsection.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(self.subsection.article, data['article'])
        self.assertEqual(self.subsection.number, data['number'])
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

    def test_unique_number_of_subsection_of_article(self):
        article = ArticleFactory()
        ArticleSubsectionFactory(article=article, number=1)
        ArticleSubsectionFactory(article=article, number=2)
        subsection = ArticleSubsectionFactory(article=article, number=3)
        subsection.number = 1
        self.assertRaisesMessage(ValidationError, 'Subsection with this number already exists.', subsection.full_clean)
        subsection.number = 2
        self.assertRaisesMessage(ValidationError, 'Subsection with this number already exists.', subsection.full_clean)
        subsection.number = 3
        subsection.full_clean()
        subsection.save()
