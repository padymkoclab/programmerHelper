
import datetime
import random

from django.core.files.base import ContentFile
from django.conf import settings

import factory
from factory import fuzzy

from mylabour.factories_utils import generate_text_by_min_length

from apps.tags.models import Tag
from apps.replies.factories import ReplyFactory

from .models import Book, Writer, NOW_YEAR


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    language = fuzzy.FuzzyChoice(tuple(code for code, name in Book.LANGUAGES))
    pages = fuzzy.FuzzyInteger(1, 1000)
    year_published = fuzzy.FuzzyInteger(1950, NOW_YEAR)

    @factory.lazy_attribute
    def picture(self):
        print(settings.MEDIA_ROOT)
        filename = 'factory_book.jpeg'
        imagefield = factory.django.ImageField()
        content = imagefield._make_data(dict(
            filename=filename, width=100, height=100, format='JPEG', color='green'
        ))
        image = ContentFile(content, filename)
        print(settings.MEDIA_ROOT)
        # import pdb; pdb.set_trace()
        return image

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


class WriterFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Writer

    name = factory.Faker('name', locale='ru')

    @factory.lazy_attribute
    def about(self):
        return generate_text_by_min_length(100, as_p=True)

    @factory.lazy_attribute
    def years_life(self):

        year = datetime.datetime.now().year

        min_year_birth = year - 16

        year_birth = random.choice((random.randint(1900, min_year_birth), '?'))

        if year_birth == '?':
            year_death = random.choice((random.randint(1915, year), '?', ''))
        else:
            year_death = random.choice((random.randint(year_birth + 16, year), '?', ''))

        return '{} - {}'.format(year_birth, year_death)
