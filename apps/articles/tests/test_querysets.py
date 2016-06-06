
from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.scopes.factories import ScopeFactory

from apps.articles.factories import articles_factory, ArticleFactory, ArticleSubsectionFactory
from apps.articles.models import Article


class ArticleQuerySetTest(TestCase):
    """

    """

    @classmethod
    def setUpTestData(self):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        articles_factory(10)

    def test_articles_with_rating(self):
        for article in Article.objects.iterator():
            article.scopes.clear()
        article1, article2, article3, article4 = Article.objects.all()[:4]
        #
        ScopeFactory(content_object=article1, scope=2)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=1)
        ScopeFactory(content_object=article1, scope=5)
        ScopeFactory(content_object=article1, scope=4)
        ScopeFactory(content_object=article1, scope=3)
        ScopeFactory(content_object=article1, scope=0)
        #
        ScopeFactory(content_object=article2, scope=1)
        ScopeFactory(content_object=article2, scope=4)
        ScopeFactory(content_object=article2, scope=2)
        #
        ScopeFactory(content_object=article3, scope=0)
        #
        articles_with_rating = Article.objects.articles_with_rating()
        self.assertEqual(articles_with_rating.get(pk=article1.pk).rating, 2.5714)
        self.assertEqual(articles_with_rating.get(pk=article2.pk).rating, 2.3333)
        self.assertEqual(articles_with_rating.get(pk=article3.pk).rating, .0)
        self.assertEqual(articles_with_rating.get(pk=article4.pk).rating, .0)

    def test_articles_with_volume(self):
        for article in Article.objects.iterator():
            article.subsections.filter().delete()
        article1, article2, article3 = Article.objects.all()[:3]
        #
        article1.header = """
For the past year and a half or so I’ve been working full-time at Dumbwaiter Design doing Django development.
I’ve picked up a bunch of useful tricks along the way that help me work, and I figured I’d share them.

I’m sure there are better ways to do some of the things that I mention.
If you know of any feel free to hit me up on Twitter and let me know.
"""
        ArticleSubsectionFactory(article=article1, number=1, title='Vagrant', content="""
I used to develop Django sites by running them on my OS X laptop locally and deploying to a Linode VPS.
I had a whole section of this post written up about tricks and tips for working with that setup.

Then I found Vagrant.

I just deleted the entire section of this post I wrote.

Vagrant gives you a better way of working. You need to use it.
        """)
        ArticleSubsectionFactory(article=article1, number=2, title='Preventing accidents', content="""
Deploying to test and staging servers should be quick and easy.
Deploying to production servers should be harder to prevent people from accidentally doing it.

I’ve created a little function that I call before deploying to production servers.
It forces me to type in random words from the system word
list before proceeding to make sure I really know what I’m doing:
        """)
        article1.conclusion = """
I hope that this longer-than-expected blog entry has given you at least one or two things to think about.

I’ve learned a lot while working with Django for Dumbwaiter every day,
but I’m sure there’s still a lot I’ve missed.
If you see something I could be doing better please let me know!
"""
        article1.full_clean()
        article1.save()
        #
        article2.header = """
In this tutorial, we will be building a Django application from the ground up
which will allow the user to query Github data through the use of a form.
To build our application, we’ll be using a wide array of technologies.
We’ll use pip for Python package dependency management, bower for front-end dependency management,
Twitter Bootstrap for design, Requests for making HTTP requests,
the Github API as our data source, and of course, Django.
"""
        ArticleSubsectionFactory(article=article2, number=1, title='Vagrant', content="""
A view is typically a visual representation of our underlying data layer (models).
Views can update models as well as retrieve data from them through a query,
which in turn would be passed to an HTML template.

In Django, views generally consist of a combination of templates, the URL dispatcher,
and a views.py file. When a user navigates to a URL, a callback function
is run which maps that particular url (such as /games) to a method named games within
views.py which may in turn query models or some external API, and finally pass that data
to a template using methods such as render.
        """)
        article2.conclusion = """
Forms are the bread and butter of web applications - every web programmer will come across them at one point or another.
Forms essentially allow users to interact with your web application through
various fields for input, usually for registration pages or in our case, performing a query.
"""
        article2.full_clean()
        article2.save()
        #
        articles_with_volume = Article.objects.articles_with_volume()
        self.assertEqual(articles_with_volume.get(pk=article1.pk).volume, 357 + 354 + 376 + 290)
        self.assertEqual(articles_with_volume.get(pk=article2.pk).volume, 446 + 598 + 291)
        self.assertEqual(articles_with_volume.get(pk=article3.pk).volume, len(article3.header) + len(article3.conclusion))

        def test_articles_with_count_comments(self):
            for article in Article.objects.iterator():
                article.comments.filter().delete()
