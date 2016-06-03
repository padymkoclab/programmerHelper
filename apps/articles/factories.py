
import random

from django.utils.text import slugify
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.comments.factories import CommentFactory
from apps.scopes.factories import ScopeFactory

from .models import *

Accounts = get_user_model().objects.all()


class ArticleFactory(factory.DjangoModelFactory):

    class Meta:
        model = Article

    quotation = factory.Faker('text', locale='ru')
    header = factory.Faker('text', locale='ru')
    conclusion = factory.Faker('text', locale='ru')
    status = fuzzy.FuzzyChoice(tuple(item[0] for item in Article.STATUS_ARTICLE))
    account = fuzzy.FuzzyChoice(Accounts)

    @factory.lazy_attribute
    def title(self):
        length_article_title = random.randint(10, 200)
        return factory.Faker('text', locale='ru').generate([])[:length_article_title]

    @factory.lazy_attribute
    def picture(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        picture = factory.Faker('slug', locale='ru').generate([])
        return '{0}{1}.gif'.format(site_name, picture)

    @factory.lazy_attribute
    def source(self):
        if random.random() > .5:
            site_name = factory.Faker('url', locale='ru').generate([])
            article_slug = slugify(self.title, allow_unicode=True)
            return '{0}{1}/'.format(site_name, article_slug)
        return

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 10)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def links(self, created, extracted, **kwargs):
        count_links = random.randrange(1, settings.MAX_COUNT_WEBLINKS_ON_OBJECT)
        weblinks = random.sample(tuple(WebLink.objects.all()), count_links)
        self.links.set(weblinks)

    @factory.post_generation
    def scopes(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 10)):
            ScopeFactory(content_object=self)


class ArticleSubsectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ArticleSubsection

    content = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def title(self):
        length_of_title_subsection_of_article = random.randint(10, 200)
        return factory.Faker('text', locale='ru').generate([])[:length_of_title_subsection_of_article]

    @factory.lazy_attribute
    def number(self):
        using_numbers = self.article.subsections.values_list('number', flat=True)
        if not using_numbers:
            return 1
        return max(using_numbers) + 1


def factory_articles(count):
    Article.objects.filter().delete()
    for i in range(count):
        article = ArticleFactory()
        for j in range(random.randrange(Article.MIN_COUNT_SUBSECTIONS, Article.MAX_COUNT_SUBSECTIONS)):
            ArticleSubsectionFactory(article=article)
