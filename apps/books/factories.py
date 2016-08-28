
import datetime
import random

from django.utils import timezone
from django.conf import settings

import factory
from factory import fuzzy

from mylabour.factories_utils import generate_text_by_min_length, generate_image, generate_words

from apps.tags.models import Tag
from apps.replies.factories import ReplyFactory

from .models import Book, Writer


NOW_YEAR = datetime.datetime.now().year


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    language = fuzzy.FuzzyChoice(tuple(code for code, name in Book.LANGUAGES))
    count_pages = fuzzy.FuzzyInteger(1, 1000)
    year_published = fuzzy.FuzzyInteger(1950, NOW_YEAR)

    @factory.lazy_attribute
    def picture(self):
        return generate_image(filename='factory_book.jpeg')

    @factory.lazy_attribute
    def name(self):
        length_book_name = random.randint(10, 100)
        return factory.Faker('text', locale='ru').generate([])[:length_book_name]

    @factory.lazy_attribute
    def publishers(self):
        return factory.Faker('text', locale='ru').generate([])[:20]

    @factory.lazy_attribute
    def description(self):
        return generate_text_by_min_length(100, as_p=True)

    @factory.lazy_attribute
    def isbn(self):
        result = list()
        for i in range(5):
            result.append(str(random.randint(10000, 11111)))
        return '-'.join(result)

    @factory.post_generation
    def replies(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            ReplyFactory(content_object=self)

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
        tags = Tag.objects.random_tags(count_tags, single_as_qs=True)
        self.tags.set(tags)

    @factory.post_generation
    def authorship(self, created, extracted, **kwargs):
        count_authors = random.randint(1, 4)

        if Writer.objects.count() < 4:
            raise ValueError('Writers is less than 4.')

        authors = random.sample(tuple(Writer.objects.all()), count_authors)
        self.authorship.set(authors)

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(days=400)).fuzz()
        self.save()


class WriterFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Writer

    name = factory.Faker('name', locale='ru')

    @factory.lazy_attribute
    def about(self):
        return generate_text_by_min_length(100)

    @factory.lazy_attribute
    def birth_year(self):
        max_birth_year = NOW_YEAR - 16
        return random.randint(1900, max_birth_year)

    @factory.lazy_attribute
    def death_year(self):
        return random.choice((random.randint(self.birth_year + 16, NOW_YEAR), None))

    @factory.lazy_attribute
    def trends(self):
        return generate_words(1, random.randint(1, 10))
