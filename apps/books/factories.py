
import datetime
import random

from django.conf import settings

import factory
from factory import fuzzy

from apps.replies.factories import Factory_Reply
from apps.scopes.factories import Factory_Scope

from .models import *


class Factory_Book(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    description = factory.Faker('text', locale='ru')
    pages = fuzzy.FuzzyInteger(1, 1000)
    year_published = fuzzy.FuzzyInteger(1950, NOW_YEAR)

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def picture(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        picture_name = factory.Faker('slug', locale='ru').generate([])
        return site_name + picture_name + 'jpeg'

    @factory.lazy_attribute
    def publishers(self):
        return factory.Faker('text', locale='ru').generate([])[:20]

    @factory.lazy_attribute
    def isbn(self):
        result = list()
        for i in range(5):
            result.append(str(random.randint(10000, 11111)))
        return '-'.join(result)

    @factory.post_generation
    def replies(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 3)):
            Factory_Reply(content_object=self)

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def links(self, created, extracted, **kwargs):
        count_links = random.randrange(0, settings.MAX_COUNT_WEBLINKS_ON_OBJECT)
        weblinks = random.sample(tuple(WebLink.objects.all()), count_links)
        self.links.set(weblinks)

    @factory.post_generation
    def scopes(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 7)):
            Factory_Scope(content_object=self)

    @factory.post_generation
    def accounts(self, created, extracted, **kwargs):
        count_authors = random.randint(1, 4)
        authors = random.sample(tuple(Writter.objects.all()), count_authors)
        self.accounts.set(authors)


class Factory_Writter(factory.django.DjangoModelFactory):

    class Meta:
        model = Writter

    name = factory.Faker('name', locale='ru')
    about = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def birthyear(self):
        now_year = datetime.datetime.now().year
        return fuzzy.FuzzyInteger(1950, now_year - 20).fuzz()

    @factory.lazy_attribute
    def deathyear(self):
        now_year = datetime.datetime.now().year
        age_writter = now_year - self.birthyear
        if random.random() > .5 and age_writter >= 50:
            return
        return fuzzy.FuzzyInteger(self.birthyear + 20, now_year).fuzz()


def factory_writters(count):
    Writter.objects.filter().delete()
    for i in range(count):
        Factory_Writter()


def factory_books(count):
    Book.objects.filter().delete()
    if not Writter.objects.count():
        factory_writters(20)
    for i in range(count):
        Factory_Book()
