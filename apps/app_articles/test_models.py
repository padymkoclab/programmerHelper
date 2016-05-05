
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import *

USER_MODEL = get_user_model()


class Factory_Article(factory.DjangoModelFactory):

    class Meta:
        model = Article

    quotation = factory.Faker('text', locale='ru')
    header = factory.Faker('text', locale='ru')
    conclusion = factory.Faker('text', locale='ru')
    status = fuzzy.FuzzyChoice(tuple(item[0] for item in Article.STATUS_ARTICLE))
    author = fuzzy.FuzzyChoice(USER_MODEL.objects.all())

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def picture(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        picture = factory.Faker('slug', locale='ru').generate([])
        return '{0}{1}.gif'.format(site_name, picture)


class Factory_OpinionAboutArticle(factory.DjangoModelFactory):

    class Meta:
        model = OpinionAboutArticle

    is_useful = fuzzy.FuzzyChoice([True, False, None])

    @factory.lazy_attribute
    def is_favorite(self):
        if self.is_useful is None:
            return OpinionAboutArticle.CHOICES_FAVORITE.unknown
        return random.choice(tuple(OpinionAboutArticle.CHOICES_FAVORITE._db_values))


class Factory_ArticleSubsection(factory.DjangoModelFactory):

    class Meta:
        model = ArticleSubsection

    article = fuzzy.FuzzyChoice(Article.objects.all())
    content = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]


class Factory_ArticleComment(factory.DjangoModelFactory):

    class Meta:
        model = ArticleComment

    text_comment = factory.Faker('text', locale='ru')
    author = fuzzy.FuzzyChoice(USER_MODEL.objects.all())
    article = fuzzy.FuzzyChoice(Article.objects.all())


Article.objects.filter().delete()
for i in range(50):
    article = Factory_Article()
    accounts = USER_MODEL.objects.all()
    # random
    count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
    count_useful_links = random.randrange(0, settings.MAX_COUNT_WEBLINKS_ON_OBJECT)
    count_users = random.randrange(0, len(accounts))
    count_subsections = random.randrange(Article.MIN_COUNT_SUBSECTIONS, Article.MAX_COUNT_SUBSECTIONS)
    count_comments = random.randrange(0, 10)
    # condition
    if count_tags > Tag.objects.count():
        count_tags = Tag.objects.count()
    if count_useful_links > WebLink.objects.count():
        count_useful_links = WebLink.objects.count()
    # getting objects
    useful_links = random.sample(tuple(WebLink.objects.all()), count_useful_links)
    tags = random.sample(tuple(Tag.objects.all()), count_tags)
    users = random.sample(tuple(accounts), count_users)
    # setting
    article.useful_links.set(useful_links)
    article.tags.set(tags)
    for user in users:
        Factory_OpinionAboutArticle(article=article, user=user)
    for i in range(count_subsections):
        Factory_ArticleSubsection(article=article)
    for i in range(count_comments):
        Factory_ArticleComment(article=article)
