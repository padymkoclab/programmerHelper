
import unittest
import statistics

from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.scopes.factories import ScopeFactory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory

from apps.books.factories import WritterFactory, books_factory
from apps.books.models import Book, Writter, NOW_YEAR


class BookQuerySetTest(TestCase):
    """
    Tests for queryset of model Book.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        books_factory(15)

    def test_books_with_count_tags(self):
        books_with_count_tags = Book.objects.books_with_count_tags()
        for book in books_with_count_tags.iterator():
            self.assertEqual(book.tags.count(), book.count_tags)

    def test_books_with_count_links(self):
        books_with_count_links = Book.objects.books_with_count_links()
        for book in books_with_count_links.iterator():
            self.assertEqual(book.links.count(), book.count_links)

    def test_books_with_count_replies(self):
        books_with_count_replies = Book.objects.books_with_count_replies()
        for book in books_with_count_replies.iterator():
            self.assertEqual(book.replies.count(), book.count_replies)

    def test_books_with_rating(self):
        # for first book rating must be 0.0
        Book.objects.first().scopes.clear()
        # for second book rating must be 0.3333, not 0.3333333... (1 / 3)
        second_book = Book.objects.all()[1]
        second_book.scopes.clear()
        ScopeFactory(content_object=second_book, scope=1)
        ScopeFactory(content_object=second_book, scope=0)
        ScopeFactory(content_object=second_book, scope=0)
        # for last book rating must be 0.4386, not 0.42857142857142855 (3 / 7)
        last_book = Book.objects.last()
        last_book.scopes.clear()
        ScopeFactory(content_object=last_book, scope=0)
        ScopeFactory(content_object=last_book, scope=0)
        ScopeFactory(content_object=last_book, scope=2)
        ScopeFactory(content_object=last_book, scope=0)
        ScopeFactory(content_object=last_book, scope=1)
        ScopeFactory(content_object=last_book, scope=0)
        ScopeFactory(content_object=last_book, scope=0)
        # checkup it
        books_with_rating = Book.objects.books_with_rating()
        for book in books_with_rating:
            scopes = book.scopes.values_list('scope', flat=True)
            mean_scope = round(statistics.mean(scopes), 4) if scopes else .0
            self.assertEqual(mean_scope, book.rating)

    def test_books_with_count_tags_links_replies_and_rating(self):
        books_with_count_tags_links_replies_and_rating = Book.objects.books_with_count_tags_links_replies_and_rating()
        for book in books_with_count_tags_links_replies_and_rating:
            self.assertEqual(book.tags.count(), book.count_tags)
            self.assertEqual(book.links.count(), book.count_links)
            self.assertEqual(book.replies.count(), book.count_replies)
            #
            scopes = book.scopes.values_list('scope', flat=True)
            mean_scope = round(statistics.mean(scopes), 4) if scopes else .0
            self.assertEqual(mean_scope, book.rating)

    def test_new_books(self):
        # no new books
        Book.objects.update(year_published=NOW_YEAR - 2)
        self.assertFalse(Book.objects.new_books())
        # all books is new (odd books published year ago, even books published in this year)
        for i, book in enumerate(Book.objects.iterator()):
            if i % 2 == 0:
                year_published = NOW_YEAR
            else:
                year_published = NOW_YEAR - 1
            book.year_published = year_published
            book.full_clean()
            book.save()
        self.assertCountEqual(Book.objects.new_books(), Book.objects.all())
        # reset
        Book.objects.update(year_published=NOW_YEAR - 10)
        self.assertFalse(Book.objects.new_books())
        # some books is new
        all_books = Book.objects.all()
        #
        first_book = all_books.first()
        second_book = all_books[1]
        penultimate_book = all_books[::-1][1]
        last_book = all_books[::-1][0]
        #
        first_book.year_published = NOW_YEAR - 1
        second_book.year_published = NOW_YEAR
        penultimate_book.year_published = NOW_YEAR - 1
        last_book.year_published = NOW_YEAR
        #
        first_book.full_clean()
        second_book.full_clean()
        penultimate_book.full_clean()
        last_book.full_clean()
        #
        first_book.save()
        second_book.save()
        penultimate_book.save()
        last_book.save()
        #
        self.assertCountEqual(Book.objects.new_books(), [first_book, second_book, penultimate_book, last_book])

    def test_giant_book(self):
        giant_books = Book.objects.giant_books()
        self.assertTrue(all(book in giant_books for book in Book.objects.iterator() if book.pages >= 500))

    def test_big_book(self):
        big_books = Book.objects.big_books()
        self.assertTrue(all(book in big_books for book in Book.objects.iterator() if 200 <= book.pages < 500))

    def test_middle_book(self):
        middle_books = Book.objects.middle_books()
        self.assertTrue(all(book in middle_books for book in Book.objects.iterator() if 50 <= book.pages < 200))

    def test_tiny_book(self):
        tiny_books = Book.objects.tiny_books()
        self.assertTrue(all(book in tiny_books for book in Book.objects.iterator() if book.pages < 50))

    def test_books_with_sizes(self):
        books_with_sizes = Book.objects.books_with_sizes()
        for book in books_with_sizes:
            if book.pages < 50:
                self.assertEqual(book.size, 'Tiny book')
            elif 50 <= book.pages < 200:
                self.assertEqual(book.size, 'Middle book')
            elif 200 <= book.pages < 500:
                self.assertEqual(book.size, 'Big book')
            else:
                self.assertEqual(book.size, 'Giant book')

    def test_popular_books(self):
        # clear all scopes in all books
        for book in Book.objects.iterator():
            book.scopes.clear()
        # get books
        book1, book2, book3, book4 = Book.objects.books_with_rating()[:4]
        # adding scopes
        #
        ScopeFactory(content_object=book1, scope=0)
        ScopeFactory(content_object=book1, scope=5)
        ScopeFactory(content_object=book1, scope=5)
        ScopeFactory(content_object=book1, scope=5)
        #
        ScopeFactory(content_object=book2, scope=5)
        ScopeFactory(content_object=book2, scope=5)
        ScopeFactory(content_object=book2, scope=5)
        #
        ScopeFactory(content_object=book3, scope=4)
        ScopeFactory(content_object=book3, scope=5)
        #
        ScopeFactory(content_object=book4, scope=5)
        #
        self.assertCountEqual(Book.objects.popular_books(), [book2, book4])

    def test_books_wrote_english(self):
        #
        Book.objects.update(language='en')
        self.assertCountEqual(Book.objects.books_wrote_english(), Book.objects.all())
        #
        Book.objects.update(language='ru')
        self.assertEqual(Book.objects.books_wrote_english().count(), 0)
        #
        first_book = Book.objects.first()
        first_book.language = 'en'
        first_book.full_clean()
        first_book.save()
        last_book = Book.objects.last()
        last_book.language = 'en'
        last_book.full_clean()
        last_book.save()
        self.assertCountEqual(Book.objects.books_wrote_english(), [first_book, last_book])

    def test_books_wrote_non_english(self):
        #
        Book.objects.update(language='ru')
        self.assertCountEqual(Book.objects.books_wrote_non_english(), Book.objects.all())
        #
        Book.objects.update(language='en')
        self.assertEqual(Book.objects.books_wrote_non_english().count(), 0)
        #
        first_book = Book.objects.first()
        first_book.language = 'uk'
        first_book.full_clean()
        first_book.save()
        last_book = Book.objects.last()
        last_book.language = 'ru'
        last_book.full_clean()
        last_book.save()
        self.assertCountEqual(Book.objects.books_wrote_non_english(), [first_book, last_book])


class WritterTest(TestCase):
    """
    Tests for queryset of model Writter.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        self.writter1 = WritterFactory(birthyear=1958, deathyear=2000)
        self.writter2 = WritterFactory(birthyear=1941, deathyear=2015)
        self.writter3 = WritterFactory(birthyear=1937, deathyear=1987)
        self.writter4 = WritterFactory(birthyear=None, deathyear=1947)
        self.writter5 = WritterFactory(birthyear=1880, deathyear=1937)
        self.writter6 = WritterFactory(birthyear=1977, deathyear=None)
        self.writter7 = WritterFactory(birthyear=1950, deathyear=None)
        self.writter8 = WritterFactory(birthyear=1911, deathyear=1990)
        self.writter9 = WritterFactory(birthyear=None, deathyear=1899)
        #
        books_factory(15)

    def test_writters_with_count_books(self):
        #
        self.writter1.books.set(Book.objects.filter()[:4])
        self.writter2.books.set(Book.objects.filter()[:1])
        self.writter3.books.clear()
        self.writter4.books.set(Book.objects.filter()[:10])
        #
        writters_with_count_books = Writter.objects.writters_with_count_books()
        self.assertEqual(writters_with_count_books.get(pk=self.writter1.pk).count_books, 4)
        self.assertEqual(writters_with_count_books.get(pk=self.writter2.pk).count_books, 1)
        self.assertEqual(writters_with_count_books.get(pk=self.writter3.pk).count_books, 0)
        self.assertEqual(writters_with_count_books.get(pk=self.writter4.pk).count_books, 10)

    def test_living_writters(self):
        #
        self.writter1.birthyear = NOW_YEAR - 100
        self.writter1.deathyear = NOW_YEAR
        self.writter1.full_clean()
        self.writter1.save()
        self.writter2.birthyear = NOW_YEAR - 50
        self.writter2.deathyear = NOW_YEAR - 1
        self.writter2.full_clean()
        self.writter2.save()
        self.writter3.birthyear = NOW_YEAR - 80
        self.writter3.deathyear = None
        self.writter3.full_clean()
        self.writter3.save()
        self.writter4.birthyear = None
        self.writter4.deathyear = None
        self.writter4.full_clean()
        self.writter4.save()
        self.writter5.birthyear = None
        self.writter5.deathyear = NOW_YEAR - 10
        self.writter5.full_clean()
        self.writter5.save()
        self.writter6.birthyear = NOW_YEAR - 30
        self.writter6.deathyear = None
        self.writter6.full_clean()
        self.writter6.save()
        self.writter7.birthyear = NOW_YEAR - 110
        self.writter7.deathyear = None
        self.writter7.full_clean()
        self.writter7.save()
        self.writter8.birthyear = NOW_YEAR - 111
        self.writter8.deathyear = None
        self.writter8.full_clean()
        self.writter8.save()
        self.writter9.birthyear = None
        self.writter9.deathyear = NOW_YEAR
        self.writter9.full_clean()
        self.writter9.save()
        #
        living_writters = Writter.objects.living_writters()
        self.assertCountEqual([self.writter3, self.writter6, self.writter7], living_writters)

    @unittest.skip('How made annotation on related field and using foward?')
    def test_writters_lived_in_range_years(self):
        self.assertCountEqual(
            [self.writter1, self.writter2, self.writter3, self.writter6, self.writter7, self.writter8],
            Writter.objects.writters_lived_in_range_years(1957, 2011))
        self.assertCountEqual(
            [self.writter2, self.writter3, self.writter5, self.writter7, self.writter8],
            Writter.objects.writters_lived_in_range_years(1930, 1950)
        )
        self.assertCountEqual(
            [self.writter1, self.writter2, self.writter6, self.writter7],
            Writter.objects.writters_lived_in_range_years(2000),
        )
        self.assertCountEqual(
            [self.writter1, self.writter2, self.writter6, self.writter7, self.writter8],
            Writter.objects.writters_lived_in_range_years(1990, 2000),
        )
        self.assertCountEqual(
            [self.writter5, self.writter9],
            Writter.objects.writters_lived_in_range_years(1800, 1900),
        )
