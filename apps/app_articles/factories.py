
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_UserComment_Generic, Factory_UserOpinion_Generic

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


class Factory_ArticleSubsection(factory.DjangoModelFactory):

    class Meta:
        model = ArticleSubsection

    article = fuzzy.FuzzyChoice(Article.objects.all())
    content = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]


Article.objects.filter().delete()
# create article
for i in range(20):
    article = Factory_Article()
    count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
    tags = random.sample(tuple(Tag.objects.all()), count_tags)
    article.tags.set(tags)
    count_useful_links = random.randrange(0, settings.MAX_COUNT_WEBLINKS_ON_OBJECT)
    useful_links = random.sample(tuple(WebLink.objects.all()), count_useful_links)
    article.useful_links.set(useful_links)
    # create subsections
    for e in range(random.randrange(Article.MIN_COUNT_SUBSECTIONS, Article.MAX_COUNT_SUBSECTIONS)):
        Factory_ArticleSubsection(article=article)
    # create opinions
    for j in range(random.randrange(0, 10)):
        Factory_UserOpinion_Generic(content_object=article)
    # create comments
    for j in range(random.randrange(0, 10)):
        Factory_UserComment_Generic(content_object=article)
