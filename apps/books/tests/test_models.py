
import unittest
import random

from django.utils import timezone
from django.utils.text import slugify
from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.replies.factories import ReplyFactory
from apps.scopes.factories import ScopeFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.utils import generate_text_by_min_length

from apps.books.factories import BookFactory, WritterFactory, books_factory, writters_factory
from apps.books.models import Book, Writter


NOW_YEAR = timezone.datetime.now().year


class BookTest(TestCase):
    """
    Test for model Book
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        writters_factory(15)

    def setUp(self):
        self.book = BookFactory()

    def test_create_book(self):
        data = dict(
            name='Книжка о программировании на Python 3',
            description=generate_text_by_min_length(100, as_p=True),
            picture='http://transcad.com/miranda.jpeg',
            language='ru',
            pages=140,
            publishers='O`Reilly',
            isbn='4515-4579-45478-78129-454',
            year_published=2007,
        )
        book = Book(**data)
        book.full_clean()
        book.save()
        #
        book.tags.add(*Tag.objects.random_tags(3))
        book.links.add(*WebLink.objects.random_weblinks(4))
        book.accounts.add(*Writter.objects.all()[:3])
        #
        ReplyFactory(content_object=book)
        ReplyFactory(content_object=book)
        ReplyFactory(content_object=book)
        for i in range(10):
            ScopeFactory(content_object=book)
        #
        book.refresh_from_db()
        self.assertEqual(book.name, data['name'])
        self.assertEqual(book.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(book.description, data['description'])
        self.assertEqual(book.picture, data['picture'])
        self.assertEqual(book.language, data['language'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])
        self.assertEqual(book.scopes.count(), 10)
        self.assertEqual(book.replies.count(), 3)
        self.assertEqual(book.tags.count(), 3)
        self.assertEqual(book.links.count(), 4)
        self.assertEqual(book.accounts.count(), 3)

    def test_update_book(self):
        # choice random language
        languages_without_already_used = filter(lambda couple: couple[0] != self.book.language, Book.LANGUAGES)
        another_language = random.choice(tuple(languages_without_already_used))[0]
        #
        data = dict(
            name='Книга рецептов JS с подробными объяснениями и красивым постраничными оформлением.',
            description=generate_text_by_min_length(100, as_p=True),
            picture='http://using.com/anaconda.png',
            language=another_language,
            pages=440,
            publishers='Express',
            isbn='785121-4512-7515-4215-784',
            year_published=2015,
        )
        book = BookFactory()
        book.name = data['name']
        book.description = data['description']
        book.picture = data['picture']
        book.language = data['language']
        book.pages = data['pages']
        book.publishers = data['publishers']
        book.isbn = data['isbn']
        book.year_published = data['year_published']
        book.full_clean()
        book.save()
        self.assertEqual(book.name, data['name'])
        self.assertEqual(book.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(book.description, data['description'])
        self.assertEqual(book.picture, data['picture'])
        self.assertEqual(book.language, data['language'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])

    def test_delete_book(self):
        self.book.delete()

    def test_unique_slug(self):
        same_name = 'Справочник смелого программиста решившегося пойти против течения и найти себя в жизни таким как есть.'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify(same_name, allow_unicode=True)
        #
        book1 = BookFactory(name=same_name_as_lower)
        book2 = BookFactory(name=same_name_as_upper)
        book3 = BookFactory(name=same_name_as_title)
        #
        self.assertEqual(book1.name, same_name_as_lower)
        self.assertEqual(book1.slug, slug_same_name)
        self.assertEqual(book2.name, same_name_as_upper)
        self.assertEqual(book2.slug, slug_same_name + '-2')
        self.assertEqual(book3.name, same_name_as_title)
        self.assertEqual(book3.slug, slug_same_name + '-3')

    def test_get_absolute_url(self):
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_rating(self):
        self.book.scopes.clear()
        self.assertEqual(self.book.get_rating(), 0)
        ScopeFactory(content_object=self.book, scope=3)
        ScopeFactory(content_object=self.book, scope=5)
        ScopeFactory(content_object=self.book, scope=1)
        ScopeFactory(content_object=self.book, scope=2)
        ScopeFactory(content_object=self.book, scope=4)
        ScopeFactory(content_object=self.book, scope=4)
        ScopeFactory(content_object=self.book, scope=1)
        ScopeFactory(content_object=self.book, scope=0)
        ScopeFactory(content_object=self.book, scope=5)
        self.assertEqual(self.book.get_rating(), 2.7778)

    def test_is_new(self):
        #
        self.book.year_published = NOW_YEAR
        self.book.full_clean()
        self.book.save()
        #
        new_book1 = BookFactory()
        new_book2 = BookFactory()
        new_book3 = BookFactory()
        new_book1.year_published = NOW_YEAR - 1
        new_book2.year_published = NOW_YEAR - 2
        new_book3.year_published = NOW_YEAR - 3
        new_book1.full_clean()
        new_book2.full_clean()
        new_book3.full_clean()
        new_book1.save()
        new_book2.save()
        new_book3.save()
        #
        self.assertTrue(self.book.is_new())
        self.assertTrue(new_book1.is_new())
        self.assertFalse(new_book2.is_new())
        self.assertFalse(new_book3.is_new())

    def test_get_size(self):
        self.book.pages = 40
        self.book.full_clean()
        self.book.save()
        self.assertEqual(self.book.get_size(), 'Tiny book')

    @unittest.skip('Have not idea how it made.')
    def test_tags_restrict(self):
        pass

    @unittest.skip('Have not idea how it made.')
    def test_links_restrict(self):
        pass


class WritterTest(TestCase):
    """
    Test for model Writter
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        books_factory(10)

    def setUp(self):
        self.writter = WritterFactory()

    def test_create_writter(self):
        data = dict(
            name='Николай Левашов',
            about=generate_text_by_min_length(100, as_p=True),
            birthyear=1960,
            deathyear=2012,
        )
        writter = Writter(**data)
        writter.full_clean()
        writter.save()
        self.assertEqual(writter.name, data['name'])
        self.assertEqual(writter.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(writter.about, data['about'])
        self.assertEqual(writter.birthyear, data['birthyear'])
        self.assertEqual(writter.deathyear, data['deathyear'])

    def test_update_writter(self):
        data = dict(
            name='Валерий Дёмин',
            about=generate_text_by_min_length(100, as_p=True),
            birthyear=1950,
            deathyear=2016,
        )
        self.writter.name = data['name']
        self.writter.about = data['about']
        self.writter.birthyear = data['birthyear']
        self.writter.deathyear = data['deathyear']
        self.writter.full_clean()
        self.writter.save()
        self.assertEqual(self.writter.name, data['name'])
        self.assertEqual(self.writter.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(self.writter.about, data['about'])
        self.assertEqual(self.writter.birthyear, data['birthyear'])
        self.assertEqual(self.writter.deathyear, data['deathyear'])

    def test_delete_writter(self):
        self.writter.delete()

    def test_unique_slug(self):
        same_name = 'русский Омар Хайам ибн Рахман Дулиб али Алькуманди Парандреус Кавказинидзе Агипян Младший'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify(same_name, allow_unicode=True)
        #
        writter1 = WritterFactory()
        writter2 = WritterFactory()
        writter3 = WritterFactory()
        #
        writter1.name = same_name_as_lower
        writter2.name = same_name_as_upper
        writter3.name = same_name_as_title
        #
        writter1.full_clean()
        writter2.full_clean()
        writter3.full_clean()
        #
        writter1.save()
        writter2.save()
        writter3.save()
        #
        self.assertEqual(writter1.name, same_name_as_lower)
        self.assertEqual(writter1.slug, slug_same_name)
        self.assertEqual(writter2.name, same_name_as_upper)
        self.assertEqual(writter2.slug, slug_same_name + '-2')
        self.assertEqual(writter3.name, same_name_as_title)
        self.assertEqual(writter3.slug, slug_same_name + '-3')

    def test_get_absolute_url(self):
        response = self.client.get(self.writter.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_if_birthyear_is_in_future(self):
        self.writter.birthyear = NOW_YEAR + 1
        self.assertRaisesMessage(ValidationError, 'Year of birth can not in future.', self.writter.full_clean)

    def test_if_deathyear_is_in_future(self):
        self.writter.deathyear = NOW_YEAR + 1
        self.assertRaisesMessage(ValidationError, 'Year of death can not in future.', self.writter.full_clean)

    def test_if_deathyear_is_more_or_equal_birthyear(self):
        self.writter.deathyear = 1990
        self.writter.birthyear = 2015
        self.assertRaisesMessage(
            ValidationError, 'Year of birth can not more or equal year of dearth.', self.writter.full_clean
        )
        self.writter.deathyear = 2014
        self.writter.birthyear = 2014
        self.assertRaisesMessage(
            ValidationError, 'Year of birth can not more or equal year of dearth.', self.writter.full_clean
        )

    def test_if_small_range_beetween_deathyear_and_birthyear(self):
        self.writter.birthyear = 1990
        self.writter.deathyear = 1999
        self.assertRaisesMessage(
            ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
        )
        self.writter.birthyear = 1990
        self.writter.deathyear = 2008
        self.assertRaisesMessage(
            ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
        )
        self.writter.birthyear = 1991
        self.writter.deathyear = 2010
        self.assertRaisesMessage(
            ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
        )
        self.writter.birthyear = 1960
        self.writter.deathyear = 1980
        self.writter.full_clean()

    def test_if_big_range_beetween_deathyear_and_birthyear(self):
        self.writter.birthyear = 1800
        self.writter.deathyear = 2000
        self.assertRaisesMessage(
            ValidationError, 'Very big range between year of birth and year of death.', self.writter.full_clean
        )
        self.writter.birthyear = 1900
        self.writter.deathyear = 2015
        self.assertRaisesMessage(
            ValidationError, 'Very big range between year of birth and year of death.', self.writter.full_clean
        )
        self.writter.birthyear = 1889
        self.writter.deathyear = 2005
        self.assertRaisesMessage(
            ValidationError, 'Very big range between year of birth and year of death.', self.writter.full_clean
        )
        self.writter.birthyear = 1890
        self.writter.deathyear = 2000
        self.writter.full_clean()
        self.writter.birthyear = 1905
        self.writter.deathyear = 2015
        self.writter.full_clean()

    def test_if_very_young_writter(self):
        self.writter.deathyear = None
        #
        self.writter.birthyear = NOW_YEAR
        self.assertRaisesMessage(ValidationError, 'Writter not possible born so early.', self.writter.full_clean)
        self.writter.birthyear = NOW_YEAR - 5
        self.assertRaisesMessage(ValidationError, 'Writter not possible born so early.', self.writter.full_clean)
        self.writter.birthyear = NOW_YEAR - 15
        self.assertRaisesMessage(ValidationError, 'Writter not possible born so early.', self.writter.full_clean)
        self.writter.birthyear = NOW_YEAR - 20
        self.writter.full_clean()

    def test_get_age_of_writter(self):
        writter1 = WritterFactory(birthyear=1950, deathyear=2013)
        writter2 = WritterFactory(birthyear=1877, deathyear=1928)
        writter3 = WritterFactory(birthyear=1990, deathyear=None)
        writter4 = WritterFactory(birthyear=None, deathyear=None)
        writter5 = WritterFactory(birthyear=None, deathyear=2016)
        writter6 = WritterFactory(birthyear=1977, deathyear=2000)
        #
        self.assertEqual(writter1.get_age(), 63)
        self.assertEqual(writter2.get_age(), 51)
        self.assertIsNone(writter3.get_age())
        self.assertIsNone(writter4.get_age())
        self.assertIsNone(writter5.get_age())
        self.assertEqual(writter6.get_age(), 23)

    def test_get_avg_scope_for_books(self):
        # without books
        self.writter.books.filter().delete()
        self.assertEqual(self.writter.get_avg_scope_for_books(), 0)
        # with single book
        book = BookFactory()
        # book.
        self.writter.books.set()
        # with many books
