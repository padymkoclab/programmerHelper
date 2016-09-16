
import random

from django.utils import timezone
from django.conf import settings

import factory
from factory import fuzzy

from utils.django.factories_utils import generate_image, generate_words, generate_text_random_length_for_field_of_model

from apps.tags.models import Tag
from apps.replies.factories import ReplyFactory

from .models import Book, Writer, Publisher


NOW_YEAR = timezone.now().year


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    language = fuzzy.FuzzyChoice(tuple(code for code, name in Book.LANGUAGES))
    count_pages = fuzzy.FuzzyInteger(1, 1500)
    year_published = fuzzy.FuzzyInteger(Book.MIN_YEAR_PUBLISHED, NOW_YEAR)

    @factory.lazy_attribute
    def publisher(self):
        return fuzzy.FuzzyChoice(Publisher.objects.all()).fuzz()

    @factory.lazy_attribute
    def image(self):
        return generate_image(filename='factory_book.jpeg')

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')

    @factory.lazy_attribute
    def isbn(self):
        result = list()
        for i in range(5):
            result.append(str(random.randint(10000, 11111)))
        return '-'.join(result)

    @factory.post_generation
    def replies(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 10)):
            ReplyFactory(content_object=self)

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag._default_manager.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def authorship(self, created, extracted, **kwargs):
        count_authors = random.randint(1, 5)
        authors = random.sample(tuple(Writer._default_manager.all()), count_authors)
        self.authorship.set(authors)

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(days=500)).fuzz()
        self.save()


class WriterFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Writer

    name = factory.Faker('name', locale='ru')
    birth_year = fuzzy.FuzzyInteger(Writer.MIN_BIRTH_YEAR, Writer.MAX_BIRTH_YEAR)

    @factory.lazy_attribute
    def about(self):
        return generate_text_random_length_for_field_of_model(self, 'about')

    @factory.lazy_attribute
    def death_year(self):
        return random.choice((random.randint(Writer.MIN_DEATH_YEAR, NOW_YEAR), None))

    @factory.lazy_attribute
    def trends(self):
        return generate_words(1, random.randint(1, 10))


class PublisherFactory(factory.DjangoModelFactory):

    class Meta:
        model = Publisher

    country_origin = fuzzy.FuzzyChoice([code for code, name in Publisher._meta.get_field('country_origin').choices])
    founded_year = fuzzy.FuzzyInteger(Publisher.MIN_FOUNDED_YEAR, NOW_YEAR)
    headquarters = factory.Faker('city')
    website = factory.Faker('url')
    name = factory.Faker('company')
