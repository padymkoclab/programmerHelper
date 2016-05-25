
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_CommentGeneric, Factory_ScopeGeneric

from .models import *

Accounts = get_user_model().objects.all()


class Factory_Article(factory.DjangoModelFactory):

    class Meta:
        model = Article

    quotation = factory.Faker('text', locale='ru')
    header = factory.Faker('text', locale='ru')
    conclusion = factory.Faker('text', locale='ru')
    status = fuzzy.FuzzyChoice(tuple(item[0] for item in Article.STATUS_ARTICLE))
    author = fuzzy.FuzzyChoice(Accounts)

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def picture(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        picture = factory.Faker('slug', locale='ru').generate([])
        return '{0}{1}.gif'.format(site_name, picture)

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 3)):
            Factory_CommentGeneric(content_object=self)

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
        for i in range(random.randint(0, 7)):
            Factory_ScopeGeneric(content_object=self)


class Factory_ArticleSubsection(factory.DjangoModelFactory):

    class Meta:
        model = ArticleSubsection

    content = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]


def factory_articles(count):
    Article.objects.filter().delete()
    for i in range(count):
        article = Factory_Article()
        for j in range(random.randrange(Article.MIN_COUNT_SUBSECTIONS, Article.MAX_COUNT_SUBSECTIONS)):
            Factory_ArticleSubsection(article=article)
