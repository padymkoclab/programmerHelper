
import random

from django.utils.text import slugify
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.comments.factories import CommentFactory
from apps.scopes.factories import ScopeFactory

from mylabour.utils import generate_text_by_min_length

from .models import *


class ArticleFactory(factory.DjangoModelFactory):

    class Meta:
        model = Article

    quotation = factory.Faker('text', locale='ru')
    status = fuzzy.FuzzyChoice(tuple(item[0] for item in Article.STATUS_ARTICLE))

    @factory.lazy_attribute
    def account(self):
        return fuzzy.FuzzyChoice(get_user_model().objects.active_accounts()).fuzz()

    @factory.lazy_attribute
    def title(self):
        length_article_title = random.randint(10, 200)
        return factory.Faker('text', locale='ru').generate([])[:length_article_title]

    @factory.lazy_attribute
    def header(self):
        return generate_text_by_min_length(200)

    @factory.lazy_attribute
    def conclusion(self):
        return generate_text_by_min_length(200)

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

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.account.date_joined).fuzz()
        self.save()
        assert self.date_added >= self.account.date_joined

    @factory.post_generation
    def date_modified(self, created, extracted, **kwargs):
        self.date_modified = fuzzy.FuzzyDateTime(self.date_added).fuzz()
        self.save()
        assert self.date_modified >= self.date_added


class ArticleSubsectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ArticleSubsection

    @factory.lazy_attribute
    def title(self):
        length_of_title_subsection_of_article = random.randint(10, 200)
        return factory.Faker('text', locale='ru').generate([])[:length_of_title_subsection_of_article]

    @factory.lazy_attribute
    def content(self):
        return generate_text_by_min_length(100, as_p=True)


def articles_factory(count):
    Article.objects.filter().delete()
    for i in range(count):
        article = ArticleFactory()
        for j in range(random.randrange(Article.MIN_COUNT_SUBSECTIONS, Article.MAX_COUNT_SUBSECTIONS)):
            ArticleSubsectionFactory(article=article)
