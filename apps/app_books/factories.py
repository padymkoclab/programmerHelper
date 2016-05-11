
import datetime
import random

from django.contrib.auth import get_user_model
from django.conf import settings

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_CommentGeneric, Factory_ScopeGeneric

from .models import *

Accounts = get_user_model().objects.all()


class Factory_Book(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    description = factory.Faker('text', locale='ru')
    pages = fuzzy.FuzzyInteger(1, 1000)
    date_published = fuzzy.FuzzyDate(
        start_date=datetime.date(2000, 1, 1),
        end_date=datetime.datetime.now().date() - datetime.timedelta(days=365),
    )
    views = fuzzy.FuzzyInteger(1000)

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
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 10)):
            Factory_CommentGeneric(content_object=self)

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def where_download(self, created, extracted, **kwargs):
        count_links = random.randrange(0, settings.MAX_COUNT_WEBLINKS_ON_OBJECT)
        weblinks = random.sample(tuple(WebLink.objects.all()), count_links)
        self.where_download.set(weblinks)

    @factory.post_generation
    def scopes(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 10)):
            Factory_ScopeGeneric(content_object=self)

    @factory.post_generation
    def authorship(self, created, extracted, **kwargs):
        count_authors = random.randint(1, 4)
        authors = random.sample(tuple(Writter.objects.all()), count_authors)
        self.authorship.set(authors)


class Factory_Writter(factory.django.DjangoModelFactory):

    class Meta:
        model = Writter

    name = factory.Faker('name', locale='ru')
    about = factory.Faker('text', locale='ru')


Writter.objects.filter().delete()
for i in range(20):
    Factory_Writter()
Book.objects.filter().delete()
for i in range(30):
    Factory_Book()
