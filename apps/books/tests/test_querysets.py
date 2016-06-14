
import unittest

from django.test import TestCase

from psycopg2.extras import NumericRange

from apps.accounts.factories import accounts_factory
from apps.replies.factories import ReplyFactory
from apps.tags.factories import tags_factory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory

from apps.books.factories import BookFactory, WritterFactory, books_factory
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
        books_factory(4)

    def setUp(self):
        books = Book.objects.all()
        self.book1 = books[0]
        self.book2 = books[1]
        self.book3 = books[2]
        self.book4 = books[3]

    def test_books_with_count_tags(self):
        #
        self.book1.tags.set(Tag.objects.random_tags(5))
        self.book2.tags.set(Tag.objects.random_tags(2))
        self.book3.tags.set([Tag.objects.random_tags(1)])
        self.book4.tags.clear()
        #
        books_with_count_tags = Book.objects.books_with_count_tags()
        #
        self.assertEqual(books_with_count_tags.get(pk=self.book1.pk).count_tags, 5)
        self.assertEqual(books_with_count_tags.get(pk=self.book2.pk).count_tags, 2)
        self.assertEqual(books_with_count_tags.get(pk=self.book3.pk).count_tags, 1)
        self.assertEqual(books_with_count_tags.get(pk=self.book4.pk).count_tags, 0)

    def test_books_with_count_links(self):
        #
        self.book1.links.set(WebLink.objects.random_weblinks(5))
        self.book2.links.set(WebLink.objects.random_weblinks(2))
        self.book3.links.set([WebLink.objects.random_weblinks(1)])
        self.book4.links.clear()
        #
        books_with_count_links = Book.objects.books_with_count_links()
        #
        self.assertEqual(books_with_count_links.get(pk=self.book1.pk).count_links, 5)
        self.assertEqual(books_with_count_links.get(pk=self.book2.pk).count_links, 2)
        self.assertEqual(books_with_count_links.get(pk=self.book3.pk).count_links, 1)
        self.assertEqual(books_with_count_links.get(pk=self.book4.pk).count_links, 0)

    def test_books_with_count_replies(self):
        #
        self.book1.replies.clear()
        self.book2.replies.clear()
        self.book3.replies.clear()
        self.book4.replies.clear()
        #
        ReplyFactory(content_object=self.book1)
        ReplyFactory(content_object=self.book1)
        ReplyFactory(content_object=self.book1)
        #
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        #
        ReplyFactory(content_object=self.book3)
        ReplyFactory(content_object=self.book3)
        #
        books_with_count_replies = Book.objects.books_with_count_replies()
        self.assertEqual(books_with_count_replies.get(pk=self.book1.pk).count_replies, 3)
        self.assertEqual(books_with_count_replies.get(pk=self.book2.pk).count_replies, 7)
        self.assertEqual(books_with_count_replies.get(pk=self.book3.pk).count_replies, 2)
        self.assertEqual(books_with_count_replies.get(pk=self.book4.pk).count_replies, 0)

    @unittest.skip('Not implemented')
    def test_books_with_rating(self):
        #
        self.book1.replies.clear()
        self.book2.replies.clear()
        self.book3.replies.clear()
        self.book4.replies.clear()
        #
        ReplyFactory(content_object=self.book1, scope_for_content=3, scope_for_style=2, scope_for_language=1)  # 2
        ReplyFactory(content_object=self.book1, scope_for_content=5, scope_for_style=2, scope_for_language=2)  # 3
        ReplyFactory(content_object=self.book1, scope_for_content=1, scope_for_style=1, scope_for_language=1)  # 1
        #
        ReplyFactory(content_object=self.book2, scope_for_content=3, scope_for_style=2, scope_for_language=1)  # 2
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=1, scope_for_language=4)  # 10 / 3
        ReplyFactory(content_object=self.book2, scope_for_content=2, scope_for_style=3, scope_for_language=2)  # 7 / 3
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=1, scope_for_language=1)  # 7 / 3
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=5, scope_for_language=5)  # 5
        #
        ReplyFactory(content_object=self.book3, scope_for_content=1, scope_for_style=5, scope_for_language=2)  # 8 / 3
        #
        books_with_rating = Book.objects.books_with_rating()
        self.assertEqual(books_with_rating.get(pk=self.book1.pk).rating, 3.0)
        self.assertEqual(books_with_rating.get(pk=self.book2.pk).rating, 14.9999)
        self.assertEqual(books_with_rating.get(pk=self.book3.pk).rating, 2.6667)
        self.assertEqual(books_with_rating.get(pk=self.book4.pk).rating, 0)

    @unittest.skip('Very complex test')
    def test_books_with_count_tags_links_replies_and_rating(self):
        self.book1.tags.set(Tag.objects.random_tags(5))
        self.book2.tags.set(Tag.objects.random_tags(2))
        self.book3.tags.set([Tag.objects.random_tags(1)])
        self.book4.tags.clear()
        #
        books_with_count_tags = Book.objects.books_with_count_tags()
        #
        self.assertEqual(books_with_count_tags.get(pk=self.book1.pk).count_tags, 5)
        self.assertEqual(books_with_count_tags.get(pk=self.book2.pk).count_tags, 2)
        self.assertEqual(books_with_count_tags.get(pk=self.book3.pk).count_tags, 1)
        self.assertEqual(books_with_count_tags.get(pk=self.book4.pk).count_tags, 0)
        #
        self.book1.links.set(WebLink.objects.random_weblinks(5))
        self.book2.links.set(WebLink.objects.random_weblinks(2))
        self.book3.links.set([WebLink.objects.random_weblinks(1)])
        self.book4.links.clear()
        #
        books_with_count_links = Book.objects.books_with_count_links()
        #
        self.assertEqual(books_with_count_links.get(pk=self.book1.pk).count_links, 5)
        self.assertEqual(books_with_count_links.get(pk=self.book2.pk).count_links, 2)
        self.assertEqual(books_with_count_links.get(pk=self.book3.pk).count_links, 1)
        self.assertEqual(books_with_count_links.get(pk=self.book4.pk).count_links, 0)
        #
        self.book1.replies.clear()
        self.book2.replies.clear()
        self.book3.replies.clear()
        self.book4.replies.clear()
        #
        ReplyFactory(content_object=self.book1)
        ReplyFactory(content_object=self.book1)
        ReplyFactory(content_object=self.book1)
        #
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        ReplyFactory(content_object=self.book2)
        #
        ReplyFactory(content_object=self.book3)
        ReplyFactory(content_object=self.book3)
        #
        books_with_count_replies = Book.objects.books_with_count_replies()
        self.assertEqual(books_with_count_replies.get(pk=self.book1.pk).count_links, 3)
        self.assertEqual(books_with_count_replies.get(pk=self.book2.pk).count_links, 7)
        self.assertEqual(books_with_count_replies.get(pk=self.book3.pk).count_links, 2)
        self.assertEqual(books_with_count_replies.get(pk=self.book4.pk).count_links, 0)
        #
        self.book1.replies.clear()
        self.book2.replies.clear()
        self.book3.replies.clear()
        self.book4.replies.clear()
        #
        ReplyFactory(content_object=self.book1, scope_for_content=3, scope_for_style=2, scope_for_language=1)  # 2
        ReplyFactory(content_object=self.book1, scope_for_content=5, scope_for_style=2, scope_for_language=2)  # 3
        ReplyFactory(content_object=self.book1, scope_for_content=1, scope_for_style=1, scope_for_language=2)  # 1
        #
        ReplyFactory(content_object=self.book2, scope_for_content=3, scope_for_style=2, scope_for_language=1)  # 2
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=1, scope_for_language=4)  # 10 / 3
        ReplyFactory(content_object=self.book2, scope_for_content=2, scope_for_style=3, scope_for_language=2)  # 7 / 3
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=1, scope_for_language=1)  # 7 / 3
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=5, scope_for_language=5)  # 5
        #
        ReplyFactory(content_object=self.book3, scope_for_content=1, scope_for_style=5, scope_for_language=2)  # 8 / 3
        #
        books_with_rating = Book.objects.books_with_rating()
        self.assertEqual(books_with_rating.get(pk=self.book1.pk).rating, 3.0)
        self.assertEqual(books_with_rating.get(pk=self.book2.pk).rating, 14.9999)
        self.assertEqual(books_with_rating.get(pk=self.book3.pk).rating, 2.6667)
        self.assertEqual(books_with_rating.get(pk=self.book4.pk).rating, 0)

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

    @unittest.skip('NotImplemented books_with_rating')
    def test_popular_books(self):
        #
        self.book1.replies.clear()
        self.book2.replies.clear()
        self.book3.replies.clear()
        self.book4.replies.clear()
        # 4.5
        ReplyFactory(content_object=self.book1, scope_for_content=5, scope_for_style=2, scope_for_language=5)  # 4
        ReplyFactory(content_object=self.book1, scope_for_content=5, scope_for_style=5, scope_for_language=4)  # 4.6667
        ReplyFactory(content_object=self.book1, scope_for_content=5, scope_for_style=4, scope_for_language=4)  # 4.3333
        ReplyFactory(content_object=self.book1, scope_for_content=5, scope_for_style=5, scope_for_language=5)  # 5
        # 3.9999
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=3, scope_for_language=5)  # 4.3333
        ReplyFactory(content_object=self.book2, scope_for_content=5, scope_for_style=2, scope_for_language=4)  # 3.6667
        # 5
        ReplyFactory(content_object=self.book3, scope_for_content=5, scope_for_style=2, scope_for_language=5)  # 4
        ReplyFactory(content_object=self.book3, scope_for_content=5, scope_for_style=5, scope_for_language=5)  # 5
        # 4
        ReplyFactory(content_object=self.book4, scope_for_content=5, scope_for_style=2, scope_for_language=5)  # 4
        #
        self.assertCountEqual(Book.objects.popular_books(), [self.book1, self.book3, self.book4])

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
        self.writter1 = WritterFactory(years_life=NumericRange(1958, 2000))
        self.writter2 = WritterFactory(years_life=NumericRange(1941, 2015))
        self.writter3 = WritterFactory(years_life=NumericRange(1937, 1987))
        self.writter4 = WritterFactory(years_life=NumericRange(None, 1947))
        self.writter5 = WritterFactory(years_life=NumericRange(1880, 1937))
        self.writter6 = WritterFactory(years_life=NumericRange(1977, None))
        self.writter7 = WritterFactory(years_life=NumericRange(1950, None))
        self.writter8 = WritterFactory(years_life=NumericRange(1911, 1990))
        self.writter9 = WritterFactory(years_life=NumericRange(None, 1899))
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

    @unittest.skip('Uncheked')
    def test_living_writters(self):
        #
        self.writter1.years_life = NumericRange(NOW_YEAR - 100, NOW_YEAR)
        self.writter1.full_clean()
        self.writter1.save()
        self.writter2.years_life = NumericRange(NOW_YEAR - 50, NOW_YEAR - 1)
        self.writter2.full_clean()
        self.writter2.save()
        self.writter3.years_life = NumericRange(NOW_YEAR - 80, None)
        self.writter3.full_clean()
        self.writter3.save()
        self.writter4.years_life = NumericRange(None, None)
        self.writter4.full_clean()
        self.writter4.save()
        self.writter5.years_life = NumericRange(None, NOW_YEAR - 10)
        self.writter5.full_clean()
        self.writter5.save()
        self.writter6.years_life = NumericRange(NOW_YEAR - 30, None)
        self.writter6.full_clean()
        self.writter6.save()
        self.writter7.years_life = NumericRange(NOW_YEAR - 110, None)
        self.writter7.full_clean()
        self.writter7.save()
        self.writter8.years_life = NumericRange(NOW_YEAR - 111, None)
        self.writter8.full_clean()
        self.writter8.save()
        self.writter9.years_life = NumericRange(None, NOW_YEAR)
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

    @unittest.skip('How made annotation on related field and using foward?')
    def test_writters_with_avg_scope_by_rating_of_books(self):
        # books of self.writter1
        self.writter1.books.clear()
        book11 = BookFactory(account=self.writter1)
        book12 = BookFactory(account=self.writter1)
        book13 = BookFactory(account=self.writter1)
        # scope for books of self.writter1
        # 3.8334
        ReplyFactory(content_object=book11, scope_for_content=5, scope_for_style=5, scope_for_language=5)  # 5
        ReplyFactory(content_object=book11, scope_for_content=3, scope_for_style=2, scope_for_language=3)  # 2.6667
        # 2.1666
        ReplyFactory(content_object=book12, scope_for_content=1, scope_for_style=1, scope_for_language=1)  # 3
        ReplyFactory(content_object=book12, scope_for_content=1, scope_for_style=2, scope_for_language=1)  # 1.3333
        # 2.6667
        ReplyFactory(content_object=book13, scope_for_content=3, scope_for_style=1, scope_for_language=1)  # 5
        ReplyFactory(content_object=book13, scope_for_content=1, scope_for_style=1, scope_for_language=1)  # 3
        # books of self.writter2
        self.writter2.books.clear()
        book21 = BookFactory(account=self.writter2)
        book22 = BookFactory(account=self.writter2)
        # scope for books of self.writter2
        # 5.6667
        ReplyFactory(content_object=book21, scope_for_content=4, scope_for_style=2, scope_for_language=2)  # 2.6667
        ReplyFactory(content_object=book21, scope_for_content=1, scope_for_style=3, scope_for_language=2)  # 3
        # 6.9999
        ReplyFactory(content_object=book22, scope_for_content=5, scope_for_style=3, scope_for_language=5)  # 4.3333
        ReplyFactory(content_object=book22, scope_for_content=1, scope_for_style=2, scope_for_language=4)  # 2.6666
        # books of self.writter3
        self.writter3.books.clear()
        book31 = BookFactory(account=self.writter3)
        # scope for books of self.writter3
        # 6.3333
        ReplyFactory(content_object=book31, scope_for_content=4, scope_for_style=1, scope_for_language=5)  # 3.3333
        ReplyFactory(content_object=book31, scope_for_content=1, scope_for_style=4, scope_for_language=4)  # 3
        #
        self.writter4.books.clear()
        book31 = BookFactory(account=self.writter3)
        #
        ReplyFactory(content_object=book31, scope_for_content=4, scope_for_style=3, scope_for_language=5)  # 4
        #
        self.writter5.books.clear()
        #
        writters_with_avg_scope_by_rating_of_books = Writter.objects.writters_with_avg_scope_by_rating_of_books()
        #
        self.assertEqual(writters_with_avg_scope_by_rating_of_books.get(pk=self.writter1.pk).avg_scope, 2.8889)
        self.assertEqual(writters_with_avg_scope_by_rating_of_books.get(pk=self.writter2.pk).avg_scope, 6.3332)
        self.assertEqual(writters_with_avg_scope_by_rating_of_books.get(pk=self.writter3.pk).avg_scope, 6.3333)
        self.assertEqual(writters_with_avg_scope_by_rating_of_books.get(pk=self.writter4.pk).avg_scope, 4)
        self.assertEqual(writters_with_avg_scope_by_rating_of_books.get(pk=self.writter5.pk).avg_scope, 0)

    @unittest.skip('How made annotation on related field and using foward?')
    def test_writters_with_count_books_and_avg_scope_by_rating_of_books(self):
        pass
