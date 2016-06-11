
import statistics
from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.scopes.factories import ScopeFactory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory

from apps.books.factories import WritterFactory, books_factory
from apps.books.models import Book, Writter


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
        """ """

        books_with_count_tags = Book.objects.books_with_count_tags()
        for book in books_with_count_tags.iterator():
            self.assertEqual(book.tags.count(), book.count_tags)

    def test_books_with_count_links(self):
        """ """

        books_with_count_links = Book.objects.books_with_count_links()
        for book in books_with_count_links.iterator():
            self.assertEqual(book.links.count(), book.count_links)

    def test_books_with_count_replies(self):
        """ """

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
        """ """

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
        """This book published in this year or one year ago."""

        raise Exception('')
        # new_books = Book.objects.new_books()
        # for book in Book.objects.iterator():
        #     if book.year_published in [NOW_YEAR, NOW_YEAR - 1]:
        #         self.assertIn(book, new_books)

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

    def test_english_wrote_books(self):
        Book.objects.made


class WritterTest(TestCase):
    """
    Tests for queryset of model Writter.
    """

    @classmethod
    def setUp(self):
        self.writter1 = WritterFactory(birthyear=1958, deathyear=2000)
        self.writter2 = WritterFactory(birthyear=1941, deathyear=2015)
        self.writter3 = WritterFactory(birthyear=1937, deathyear=1987)
        self.writter4 = WritterFactory(birthyear=1897, deathyear=1947)
        self.writter5 = WritterFactory(birthyear=1880, deathyear=1937)
        self.writter6 = WritterFactory(birthyear=1977, deathyear=None)
        self.writter7 = WritterFactory(birthyear=1950, deathyear=None)
        self.writter8 = WritterFactory(birthyear=1911, deathyear=1990)
        self.writter9 = WritterFactory(birthyear=1850, deathyear=1899)

    def test_writters_with_count_books(self):
        for writter in Writter.objects.writters_with_count_books().iterator():
            self.assertEqual(writter.count_books, writter.books.count())

    def test_living_writters(self):
        living_writters = Writter.objects.living_writters()
        for writter in Writter.objects.iterator():
            if not writter.deathyear:
                self.assertIn(writter, living_writters)
            else:
                self.assertNotIn(writter, living_writters)

    def test_writters_lived_in_range_years(self):
        self.assertCountEqual(
            [self.writter1, self.writter2, self.writter3, self.writter6, self.writter7, self.writter8],
            Writter.objects.writters_lived_in_range_years(1957, 2011))
        self.assertCountEqual(
            [self.writter2, self.writter3, self.writter4, self.writter5, self.writter7, self.writter8],
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
            [self.writter4, self.writter5, self.writter9],
            Writter.objects.writters_lived_in_range_years(1800, 1900),
        )
