
import random

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

import factory
from factory import fuzzy

from utils.django.factories_utils import (
    generate_image,
    generate_words,
    generate_text_random_length_for_field_of_model,
)

from apps.tags.models import Tag

from .models import Book, Writer, Publisher, Reply


NOW_YEAR = timezone.now().year


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    language = fuzzy.FuzzyChoice([code for code, name in Book.LANGUAGES])
    count_pages = fuzzy.FuzzyInteger(1, 1500)
    year_published = fuzzy.FuzzyInteger(Book.MIN_YEAR_PUBLISHED, NOW_YEAR)
    publisher = fuzzy.FuzzyChoice(Publisher.objects.all())

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
            ReplyFactory(book=self)

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
    def created(self, created, extracted, **kwargs):

        created = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(days=500)).fuzz()
        self.created = created
        self.full_clean()
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
        return random.choice((random.randint(self.birth_year, NOW_YEAR), None))

    @factory.lazy_attribute
    def trends(self):
        return generate_words(1, random.randint(1, 10))


class PublisherFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Publisher

    country_origin = fuzzy.FuzzyChoice([code for code, name in Publisher._meta.get_field('country_origin').choices])
    founded_year = fuzzy.FuzzyInteger(Publisher.MIN_FOUNDED_YEAR, NOW_YEAR)
    headquarters = factory.Faker('city')
    website = factory.Faker('url')
    name = factory.Faker('company')


class ReplyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Reply

    text_reply = factory.Faker('text', locale='ru')
    mark_for_language = fuzzy.FuzzyInteger(1, 5)
    mark_for_content = fuzzy.FuzzyInteger(1, 5)
    mark_for_style = fuzzy.FuzzyInteger(1, 5)

    @factory.lazy_attribute
    def user(self):

        users_given_their_replies = self.book.replies.values('user__pk')
        users_given_not_their_replies = get_user_model().objects.exclude(pk__in=users_given_their_replies)
        return users_given_not_their_replies.random_users(1)

    @factory.lazy_attribute
    def advantages(self):

        return generate_words(1, 10, 'title')

    @factory.lazy_attribute
    def disadvantages(self):

        return generate_words(1, 10, 'title')

    @factory.post_generation
    def created(self, created, extracted, **kwargs):

        min_possible_created = max(self.user.date_joined, self.book.created)
        created = fuzzy.FuzzyDateTime(min_possible_created).fuzz()
        self.created = created
        self.save()
