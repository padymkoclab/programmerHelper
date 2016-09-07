
from unittest import mock

import pytest

from utils.django.test_utils import EnhancedTestCase

from apps.replies.factories import ReplyFactory
from apps.tags.models import Tag

from apps.books.models import Book, Writer


class BookQuerySetTests(EnhancedTestCase):
    """
    Tests for queryset of the model Book.
    """

    @classmethod
    def setUpTestData(cls):
        cls.call_command('factory_test_users', '8')
        cls.call_command('factory_test_writers', '4')
        cls.call_command('factory_test_books', '7')

        cls.book1, cls.book2, cls.book3, cls.book4, cls.book5, cls.book6, cls.book7 = Book.objects.all()

        for book in Book.objects.iterator():
            book.replies.clear()
            book.tags.clear()

        cls.book1.language = 'ru'
        cls.book1.year_published = 2003
        cls.book1.full_clean()
        cls.book1.save()

        cls.book2.language = 'en'
        cls.book2.year_published = 2002
        cls.book2.full_clean()
        cls.book2.save()

        cls.book3.language = 'ru'
        cls.book3.year_published = 2004
        cls.book3.full_clean()
        cls.book3.save()

        cls.book4.language = 'en'
        cls.book4.year_published = 2001
        cls.book4.full_clean()
        cls.book4.save()

        cls.book5.language = 'en'
        cls.book5.year_published = 2006
        cls.book5.full_clean()
        cls.book5.save()

        cls.book6.language = 'ru'
        cls.book6.year_published = 2000
        cls.book6.full_clean()
        cls.book6.save()

        cls.book7.language = 'en'
        cls.book7.year_published = 2005
        cls.book7.full_clean()
        cls.book7.save()

    def setUp(self):
        for book in Book.objects.iterator():
            book.refresh_from_db()

    def test_books_with_count_tags_if_books_have_not_tags(self):

        books_with_count_tags = Book.objects.books_with_count_tags()
        for book in Book.objects.iterator():
            self.assertEqual(books_with_count_tags.get(pk=book.pk).count_tags, 0)

    def test_books_with_count_tags_if_books_have_tags(self):

        self.book1.tags.set(Tag.objects.random_tags(5))
        self.book2.tags.set(Tag.objects.random_tags(2))
        self.book3.tags.set(Tag.objects.random_tags(1, single_as_qs=True))
        self.book4.tags.set(Tag.objects.random_tags(4))
        self.book6.tags.set(Tag.objects.random_tags(3))
        self.book7.tags.set(Tag.objects.random_tags(6))

        books_with_count_tags = Book.objects.books_with_count_tags()
        self.assertEqual(books_with_count_tags.get(pk=self.book1.pk).count_tags, 5)
        self.assertEqual(books_with_count_tags.get(pk=self.book2.pk).count_tags, 2)
        self.assertEqual(books_with_count_tags.get(pk=self.book3.pk).count_tags, 1)
        self.assertEqual(books_with_count_tags.get(pk=self.book4.pk).count_tags, 4)
        self.assertEqual(books_with_count_tags.get(pk=self.book5.pk).count_tags, 0)
        self.assertEqual(books_with_count_tags.get(pk=self.book6.pk).count_tags, 3)
        self.assertEqual(books_with_count_tags.get(pk=self.book7.pk).count_tags, 6)

    def test_books_with_count_replies_if_books_have_not_replies(self):

        books_with_count_replies = Book.objects.books_with_count_replies()
        for book in Book.objects.iterator():
            self.assertEqual(books_with_count_replies.get(pk=book.pk).count_replies, 0)

    def test_books_with_count_replies_if_books_have_replies(self):

        for book, count_replies in (
            (self.book1, 3),
            (self.book2, 6),
            (self.book3, 2),
            (self.book4, 1),
            (self.book5, 0),
            (self.book6, 4),
            (self.book7, 6),
        ):
            for i in range(count_replies):
                ReplyFactory(content_object=book)

        books_with_count_replies = Book.objects.books_with_count_replies()
        self.assertEqual(books_with_count_replies.get(pk=self.book1.pk).count_replies, 3)
        self.assertEqual(books_with_count_replies.get(pk=self.book2.pk).count_replies, 6)
        self.assertEqual(books_with_count_replies.get(pk=self.book3.pk).count_replies, 2)
        self.assertEqual(books_with_count_replies.get(pk=self.book4.pk).count_replies, 1)
        self.assertEqual(books_with_count_replies.get(pk=self.book5.pk).count_replies, 0)
        self.assertEqual(books_with_count_replies.get(pk=self.book6.pk).count_replies, 4)
        self.assertEqual(books_with_count_replies.get(pk=self.book7.pk).count_replies, 6)

    def test_books_with_rating_if_books_have_no_replies(self):

        books_with_rating = Book.objects.books_with_rating()
        for book in Book.objects.iterator():
            self.assertEqual(books_with_rating.get(pk=book.pk).rating, .0)

    def test_books_with_rating_if_books_have_replies(self):

        # total mark 3.0
        ReplyFactory(content_object=self.book1, mark_for_content=3, mark_for_style=2, mark_for_language=1)  # 2
        ReplyFactory(content_object=self.book1, mark_for_content=5, mark_for_style=2, mark_for_language=2)  # 3
        ReplyFactory(content_object=self.book1, mark_for_content=1, mark_for_style=1, mark_for_language=1)  # 1

        # total mark 3.733
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=1, mark_for_language=4)  # 10 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=2, mark_for_style=4, mark_for_language=2)  # 8 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=5, mark_for_language=1)  # 11 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=3, mark_for_language=5)  # 13 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=5, mark_for_language=4)  # 14 / 3

        # total mark 0.0
        ReplyFactory(content_object=self.book3, mark_for_content=0, mark_for_style=0, mark_for_language=0)  # 0

        # total mark 2.833
        ReplyFactory(content_object=self.book4, mark_for_content=2, mark_for_style=5, mark_for_language=1)  # 2.667
        ReplyFactory(content_object=self.book4, mark_for_content=5, mark_for_style=3, mark_for_language=2)  # 3

        # total mark 2.667
        ReplyFactory(content_object=self.book5, mark_for_content=5, mark_for_style=5, mark_for_language=2)  # 2.667

        # total mark 4.5
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=4)  # 14 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=3, mark_for_language=5)  # 13 / 3

        books_with_rating = Book.objects.books_with_rating()
        self.assertEqual(books_with_rating.get(pk=self.book1.pk).rating, 3.0)
        self.assertEqual(books_with_rating.get(pk=self.book2.pk).rating, 3.733)
        self.assertEqual(books_with_rating.get(pk=self.book3.pk).rating, 0.0)
        self.assertEqual(books_with_rating.get(pk=self.book4.pk).rating, 2.833)
        self.assertEqual(books_with_rating.get(pk=self.book5.pk).rating, 2.667)
        self.assertEqual(books_with_rating.get(pk=self.book6.pk).rating, 4.5)
        self.assertEqual(books_with_rating.get(pk=self.book7.pk).rating, 0.0)

    def test_books_with_count_tags_replies_and_rating_if_books_have_not_tags_and_replies(self):

        books_with_count_tags_replies_and_rating = Book.objects.books_with_count_tags_replies_and_rating()
        for book in Book.objects.iterator():
            book = books_with_count_tags_replies_and_rating.get(pk=book.pk)
            self.assertEqual(book.rating, .0)
            self.assertEqual(book.count_tags, 0)
            self.assertEqual(book.count_replies, 0)

    def test_books_with_count_tags_replies_and_rating_if_books_have_tags_and_replies(self):

        # Add tags
        #
        self.book1.tags.set(Tag.objects.random_tags(6))
        self.book2.tags.set(Tag.objects.random_tags(5))
        self.book3.tags.set(Tag.objects.random_tags(4))
        self.book4.tags.set(Tag.objects.random_tags(3))
        self.book5.tags.set(Tag.objects.random_tags(2))
        self.book6.tags.set(Tag.objects.random_tags(1, single_as_qs=True))

        # Add replies with marks
        #
        # total mark 4.667
        ReplyFactory(content_object=self.book1, mark_for_content=3, mark_for_style=3, mark_for_language=3)  # 3
        ReplyFactory(content_object=self.book1, mark_for_content=5, mark_for_style=2, mark_for_language=2)  # 3
        ReplyFactory(content_object=self.book1, mark_for_content=1, mark_for_style=5, mark_for_language=2)  # 8

        # total mark 3.0
        ReplyFactory(content_object=self.book2, mark_for_content=3, mark_for_style=2, mark_for_language=1)  # 2
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=1, mark_for_language=4)  # 10 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=2, mark_for_style=3, mark_for_language=2)  # 7 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=1, mark_for_language=1)  # 7 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5

        # total mark 3.333
        ReplyFactory(content_object=self.book3, mark_for_content=3, mark_for_style=5, mark_for_language=2)  # 10 / 3

        # total mark 3.5
        ReplyFactory(content_object=self.book4, mark_for_content=1, mark_for_style=3, mark_for_language=5)  # 3
        ReplyFactory(content_object=self.book4, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4

        # total mark 3.167
        ReplyFactory(content_object=self.book5, mark_for_content=1, mark_for_style=5, mark_for_language=2)  # 8 / 3
        ReplyFactory(content_object=self.book5, mark_for_content=2, mark_for_style=2, mark_for_language=5)  # 3
        ReplyFactory(content_object=self.book5, mark_for_content=1, mark_for_style=5, mark_for_language=1)  # 7 / 3
        ReplyFactory(content_object=self.book5, mark_for_content=5, mark_for_style=4, mark_for_language=5)  # 14 / 3

        # total mark 2.833
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=5, mark_for_language=3)  # 8 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=3, mark_for_language=2)  # 2
        ReplyFactory(content_object=self.book6, mark_for_content=2, mark_for_style=1, mark_for_language=1)  # 4 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=5, mark_for_language=5)  # 11 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=4, mark_for_style=4, mark_for_language=5)  # 14 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=5, mark_for_language=2)  # 8 / 3

        # Tests
        books_with_count_tags_replies_and_rating = Book.objects.books_with_count_tags_replies_and_rating()
        result_book1 = books_with_count_tags_replies_and_rating.get(pk=self.book1.pk)
        result_book2 = books_with_count_tags_replies_and_rating.get(pk=self.book2.pk)
        result_book3 = books_with_count_tags_replies_and_rating.get(pk=self.book3.pk)
        result_book4 = books_with_count_tags_replies_and_rating.get(pk=self.book4.pk)
        result_book5 = books_with_count_tags_replies_and_rating.get(pk=self.book5.pk)
        result_book6 = books_with_count_tags_replies_and_rating.get(pk=self.book6.pk)
        result_book7 = books_with_count_tags_replies_and_rating.get(pk=self.book7.pk)

        self.assertEqual(result_book1.rating, 4.667)
        self.assertEqual(result_book2.rating, 3.0)
        self.assertEqual(result_book3.rating, 3.333)
        self.assertEqual(result_book4.rating, 3.5)
        self.assertEqual(result_book5.rating, 3.167)
        self.assertEqual(result_book6.rating, 2.833)
        self.assertEqual(result_book7.rating, 0.0)

        self.assertEqual(result_book1.count_tags, 6)
        self.assertEqual(result_book2.count_tags, 5)
        self.assertEqual(result_book3.count_tags, 4)
        self.assertEqual(result_book4.count_tags, 3)
        self.assertEqual(result_book5.count_tags, 2)
        self.assertEqual(result_book6.count_tags, 1)
        self.assertEqual(result_book7.count_tags, 0)

        self.assertEqual(result_book1.count_replies, 3)
        self.assertEqual(result_book2.count_replies, 5)
        self.assertEqual(result_book3.count_replies, 1)
        self.assertEqual(result_book4.count_replies, 2)
        self.assertEqual(result_book5.count_replies, 4)
        self.assertEqual(result_book6.count_replies, 6)
        self.assertEqual(result_book7.count_replies, 0)

    @mock.patch('django.utils.timezone.now')
    def test_new_books(self, mock_now):

        mock_now.return_value = self.timezone.datetime(2006, 1, 1)
        new_books = Book.objects.new_books()
        self.assertCountEqual(new_books, [self.book5, self.book7])

    def test_tiny_book(self):

        self.book1.pages = 1
        self.book1.full_clean()
        self.book1.save()

        self.book2.pages = 100
        self.book2.full_clean()
        self.book2.save()

        self.book3.pages = 70
        self.book3.full_clean()
        self.book3.save()

        self.book4.pages = 49
        self.book4.full_clean()
        self.book4.save()

        self.book5.pages = 50
        self.book5.full_clean()
        self.book5.save()

        self.book6.pages = 10
        self.book6.full_clean()
        self.book6.save()

        self.book7.pages = 200
        self.book7.full_clean()
        self.book7.save()

        self.assertCountEqual(Book.objects.tiny_books(), [self.book1, self.book4, self.book6])

    def test_middle_book(self):

        self.book1.pages = 200
        self.book1.full_clean()
        self.book1.save()

        self.book2.pages = 100
        self.book2.full_clean()
        self.book2.save()

        self.book3.pages = 300
        self.book3.full_clean()
        self.book3.save()

        self.book4.pages = 400
        self.book4.full_clean()
        self.book4.save()

        self.book5.pages = 49
        self.book5.full_clean()
        self.book5.save()

        self.book6.pages = 299
        self.book6.full_clean()
        self.book6.save()

        self.book7.pages = 50
        self.book7.full_clean()
        self.book7.save()

        self.assertCountEqual(Book.objects.middle_books(), [self.book1, self.book2, self.book6, self.book7])

    def test_big_book(self):

        self.book1.pages = 200
        self.book1.full_clean()
        self.book1.save()

        self.book2.pages = 900
        self.book2.full_clean()
        self.book2.save()

        self.book3.pages = 300
        self.book3.full_clean()
        self.book3.save()

        self.book4.pages = 1100
        self.book4.full_clean()
        self.book4.save()

        self.book5.pages = 1000
        self.book5.full_clean()
        self.book5.save()

        self.book6.pages = 299
        self.book6.full_clean()
        self.book6.save()

        self.book7.pages = 600
        self.book7.full_clean()
        self.book7.save()

        self.assertCountEqual(Book.objects.big_books(), [self.book2, self.book3, self.book7])

    def test_great_book(self):

        self.book1.pages = 200
        self.book1.full_clean()
        self.book1.save()

        self.book2.pages = 1100
        self.book2.full_clean()
        self.book2.save()

        self.book3.pages = 300
        self.book3.full_clean()
        self.book3.save()

        self.book4.pages = 1000
        self.book4.full_clean()
        self.book4.save()

        self.book5.pages = 999
        self.book5.full_clean()
        self.book5.save()

        self.book6.pages = 299
        self.book6.full_clean()
        self.book6.save()

        self.book7.pages = 600
        self.book7.full_clean()
        self.book7.save()

        self.assertCountEqual(Book.objects.great_books(), [self.book2, self.book4])

    def test_books_with_sizes(self):

        self.book1.pages = 49
        self.book1.full_clean()
        self.book1.save()

        self.book2.pages = 50
        self.book2.full_clean()
        self.book2.save()

        self.book3.pages = 299
        self.book3.full_clean()
        self.book3.save()

        self.book4.pages = 599
        self.book4.full_clean()
        self.book4.save()

        self.book5.pages = 1000
        self.book5.full_clean()
        self.book5.save()

        self.book6.pages = 999
        self.book6.full_clean()
        self.book6.save()

        self.book7.pages = 300
        self.book7.full_clean()
        self.book7.save()

        books_with_sizes = Book.objects.books_with_sizes()
        self.assertEqual(books_with_sizes.get(pk=self.book1.pk).size, 'Tiny book')
        self.assertEqual(books_with_sizes.get(pk=self.book2.pk).size, 'Middle book')
        self.assertEqual(books_with_sizes.get(pk=self.book3.pk).size, 'Middle book')
        self.assertEqual(books_with_sizes.get(pk=self.book4.pk).size, 'Big book')
        self.assertEqual(books_with_sizes.get(pk=self.book5.pk).size, 'Great book')
        self.assertEqual(books_with_sizes.get(pk=self.book6.pk).size, 'Big book')
        self.assertEqual(books_with_sizes.get(pk=self.book7.pk).size, 'Big book')

    def test_popular_books_if_books_have_not_replies(self):

        self.assertQuerysetEqual(Book.objects.popular_books(), Book.objects.none())

    def test_popular_books_if_books_have_replies(self):

        # total mark is 4.5
        ReplyFactory(content_object=self.book1, mark_for_content=5, mark_for_style=5, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book1, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5

        # total mark is 3.917
        ReplyFactory(content_object=self.book2, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=4, mark_for_language=5)  # 14 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book2, mark_for_content=3, mark_for_style=3, mark_for_language=3)  # 3

        # total mark is 5
        ReplyFactory(content_object=self.book3, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5

        # total mark is 4
        ReplyFactory(content_object=self.book4, mark_for_content=5, mark_for_style=3, mark_for_language=4)  # 4

        # total mark is 3.5
        ReplyFactory(content_object=self.book5, mark_for_content=1, mark_for_style=1, mark_for_language=1)  # 3
        ReplyFactory(content_object=self.book5, mark_for_content=1, mark_for_style=2, mark_for_language=1)  # 4

        # total mark is 4.944
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=4, mark_for_language=5)  # 14 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5

        self.assertCountEqual(
            Book.objects.popular_books(),
            [self.book1, self.book3, self.book4, self.book6]
        )

    def test_books_wrote_on_english(self):

        books_wrote_on_english = Book.objects.books_wrote_on_english()
        self.assertCountEqual(books_wrote_on_english, (self.book2, self.book4, self.book5, self.book7))

    def test_books_wrote_on_russian(self):

        books_wrote_on_russian = Book.objects.books_wrote_on_russian()
        self.assertCountEqual(books_wrote_on_russian, (self.book1, self.book3, self.book6))


class WriterQuerySetTests(EnhancedTestCase):
    """
    Tests for queryset of the model Writer.
    """

    @classmethod
    def setUpTestData(cls):
        cls.call_command('factory_test_users', '8')
        cls.call_command('factory_test_writers', '9')
        cls.call_command('factory_test_books', '8')

        cls.writer1, cls.writer2, cls.writer3, cls.writer4,\
            cls.writer5, cls.writer6, cls.writer7, cls.writer8, cls.writer9 = Writer.objects.all()

        cls.book1, cls.book2, cls.book3, cls.book4,\
            cls.book5, cls.book6, cls.book7, cls.book8 = Book.objects.all()

        for book in Book.objects.iterator():
            book.replies.clear()

        cls.writer1.years_life = '1900 - 2000'
        cls.writer1.books.set([cls.book1, cls.book2, cls.book3, cls.book4])
        cls.writer1.full_clean()
        cls.writer1.save()

        cls.writer2.years_life = '1999 - 2016'
        cls.writer2.books.set([cls.book1])
        cls.writer2.full_clean()
        cls.writer2.save()

        cls.writer3.years_life = '1900 - 1999'
        cls.writer3.books.set([cls.book1, cls.book2, cls.book3, cls.book4, cls.book5, cls.book6])
        cls.writer3.full_clean()
        cls.writer3.save()

        cls.writer4.years_life = '? - 1999'
        cls.writer4.books.set([cls.book5, cls.book6])
        cls.writer4.full_clean()
        cls.writer4.save()

        cls.writer5.years_life = '2000 - '
        cls.writer5.books.set([cls.book5, cls.book6, cls.book7])
        cls.writer5.full_clean()
        cls.writer5.save()

        cls.writer6.years_life = '1999 - ?'
        cls.writer6.books.clear()
        cls.writer6.full_clean()
        cls.writer6.save()

        cls.writer7.years_life = '1999 - '
        cls.writer7.books.set([cls.book4, cls.book5, cls.book6, cls.book7, cls.book8])
        cls.writer7.full_clean()
        cls.writer7.save()

        cls.writer8.years_life = '2000 - 2016'
        cls.writer8.books.set([cls.book1, cls.book2, cls.book3, cls.book4, cls.book5, cls.book6, cls.book7, cls.book8])
        cls.writer8.full_clean()
        cls.writer8.save()

        cls.writer9.years_life = '? - ?'
        cls.writer9.books.set([cls.book2, cls.book3, cls.book4, cls.book5, cls.book6, cls.book7, cls.book8])
        cls.writer9.full_clean()
        cls.writer9.save()

    def setUp(self):

        for book in Book.objects.iterator():
            book.refresh_from_db()
        for writer in Writer.objects.iterator():
            writer.refresh_from_db()

    def test_writers_with_count_books_if_writers_have_no_books(self):

        Book.objects.filter().delete()

        writers_with_count_books = Writer.objects.writers_with_count_books()
        self.assertEqual(writers_with_count_books.get(pk=self.writer1.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer2.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer3.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer4.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer5.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer6.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer7.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer8.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer9.pk).count_books, 0)

    def test_writers_with_count_books_if_writers_have_books(self):

        writers_with_count_books = Writer.objects.writers_with_count_books()
        self.assertEqual(writers_with_count_books.get(pk=self.writer1.pk).count_books, 4)
        self.assertEqual(writers_with_count_books.get(pk=self.writer2.pk).count_books, 1)
        self.assertEqual(writers_with_count_books.get(pk=self.writer3.pk).count_books, 6)
        self.assertEqual(writers_with_count_books.get(pk=self.writer4.pk).count_books, 2)
        self.assertEqual(writers_with_count_books.get(pk=self.writer5.pk).count_books, 3)
        self.assertEqual(writers_with_count_books.get(pk=self.writer6.pk).count_books, 0)
        self.assertEqual(writers_with_count_books.get(pk=self.writer7.pk).count_books, 5)
        self.assertEqual(writers_with_count_books.get(pk=self.writer8.pk).count_books, 8)
        self.assertEqual(writers_with_count_books.get(pk=self.writer9.pk).count_books, 7)

    def test_writers_20th_century(self):

        self.assertCountEqual(
            Writer.objects.writers_20th_century(),
            [self.writer1, self.writer2, self.writer3, self.writer4, self.writer6, self.writer7]
        )

    def test_writers_21st_century(self):

        self.assertCountEqual(
            Writer.objects.writers_21st_century(),
            [self.writer1, self.writer2, self.writer5, self.writer7, self.writer8]
        )

    def tests_writers_with_avg_mark_by_rating_of_books_if_books_have_not_replies(self):

        writers_with_avg_mark_by_rating_of_books = Writer.objects.writers_with_avg_mark_by_rating_of_books()
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer1.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer2.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer3.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer4.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer5.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer6.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer7.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer8.pk).rating_books, .0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer9.pk).rating_books, .0)

    def tests_writers_with_avg_mark_by_rating_of_books_if_books_have_replies(self):

        # Add replies to books

        # 1.333
        ReplyFactory(content_object=self.book1, mark_for_content=1, mark_for_style=2, mark_for_language=1)  # 1

        # 3
        ReplyFactory(content_object=self.book2, mark_for_content=1, mark_for_style=1, mark_for_language=3)  # 5 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=1, mark_for_style=2, mark_for_language=4)  # 7 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5

        # 3.5
        ReplyFactory(content_object=self.book3, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book3, mark_for_content=1, mark_for_style=1, mark_for_language=1)  # 3

        # 2.333
        ReplyFactory(content_object=self.book4, mark_for_content=4, mark_for_style=3, mark_for_language=1)  # 8 / 3
        ReplyFactory(content_object=self.book4, mark_for_content=1, mark_for_style=2, mark_for_language=2)  # 5 / 3
        ReplyFactory(content_object=self.book4, mark_for_content=4, mark_for_style=3, mark_for_language=1)  # 8 / 3

        # 2.75
        ReplyFactory(content_object=self.book5, mark_for_content=1, mark_for_style=1, mark_for_language=1)  # 1
        ReplyFactory(content_object=self.book5, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book5, mark_for_content=5, mark_for_style=3, mark_for_language=2)  # 10 / 3
        ReplyFactory(content_object=self.book5, mark_for_content=2, mark_for_style=2, mark_for_language=4)  # 8 / 3

        # 3.067
        ReplyFactory(content_object=self.book6, mark_for_content=3, mark_for_style=1, mark_for_language=1)  # 5 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=4)  # 14 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=3, mark_for_language=2)  # 3
        ReplyFactory(content_object=self.book6, mark_for_content=4, mark_for_style=1, mark_for_language=1)  # 3
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=2, mark_for_language=3)  # 3

        # 4.333
        ReplyFactory(content_object=self.book7, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book7, mark_for_content=5, mark_for_style=5, mark_for_language=4)  # 14 / 3

        # 1.667
        ReplyFactory(content_object=self.book8, mark_for_content=2, mark_for_style=2, mark_for_language=1)  # 3

        writers_with_avg_mark_by_rating_of_books = Writer.objects.writers_with_avg_mark_by_rating_of_books()
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer1.pk).avg_mark, 2.542)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer2.pk).avg_mark, 1.333)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer3.pk).avg_mark, 2.664)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer4.pk).avg_mark, 2.908)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer5.pk).avg_mark, 3.383)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer6.pk).avg_mark, 0)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer7.pk).avg_mark, 2.83)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer8.pk).avg_mark, 2.748)
        self.assertEqual(writers_with_avg_mark_by_rating_of_books.get(pk=self.writer9.pk).avg_mark, 2.95)

    def test_writers_with_count_books_and_avg_mark_by_rating_of_books(self):

        # Add replies to books

        # 1.333
        ReplyFactory(content_object=self.book1, mark_for_content=1, mark_for_style=2, mark_for_language=1)  # 1

        # 3
        ReplyFactory(content_object=self.book2, mark_for_content=1, mark_for_style=1, mark_for_language=3)  # 5 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=1, mark_for_style=2, mark_for_language=4)  # 7 / 3
        ReplyFactory(content_object=self.book2, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5

        # 3.5
        ReplyFactory(content_object=self.book3, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book3, mark_for_content=1, mark_for_style=1, mark_for_language=1)  # 3

        # 2.333
        ReplyFactory(content_object=self.book4, mark_for_content=4, mark_for_style=3, mark_for_language=1)  # 8 / 3
        ReplyFactory(content_object=self.book4, mark_for_content=1, mark_for_style=2, mark_for_language=2)  # 5 / 3
        ReplyFactory(content_object=self.book4, mark_for_content=4, mark_for_style=3, mark_for_language=1)  # 8 / 3

        # 2.75
        ReplyFactory(content_object=self.book5, mark_for_content=1, mark_for_style=1, mark_for_language=1)  # 1
        ReplyFactory(content_object=self.book5, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book5, mark_for_content=5, mark_for_style=3, mark_for_language=2)  # 10 / 3
        ReplyFactory(content_object=self.book5, mark_for_content=2, mark_for_style=2, mark_for_language=4)  # 8 / 3

        # 3.067
        ReplyFactory(content_object=self.book6, mark_for_content=3, mark_for_style=1, mark_for_language=1)  # 5 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=5, mark_for_style=5, mark_for_language=4)  # 14 / 3
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=3, mark_for_language=2)  # 3
        ReplyFactory(content_object=self.book6, mark_for_content=4, mark_for_style=1, mark_for_language=1)  # 3
        ReplyFactory(content_object=self.book6, mark_for_content=1, mark_for_style=2, mark_for_language=3)  # 3

        # 4.333
        ReplyFactory(content_object=self.book7, mark_for_content=4, mark_for_style=4, mark_for_language=4)  # 4
        ReplyFactory(content_object=self.book7, mark_for_content=5, mark_for_style=5, mark_for_language=4)  # 14 / 3

        # 1.667
        ReplyFactory(content_object=self.book8, mark_for_content=2, mark_for_style=2, mark_for_language=1)  # 3

        writers_with_count_books_and_avg_mark_by_rating_of_books = \
            Writer.objects.writers_with_count_books_and_avg_mark_by_rating_of_books()

        writer1 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer1.pk)
        writer2 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer2.pk)
        writer3 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer3.pk)
        writer4 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer4.pk)
        writer5 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer5.pk)
        writer6 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer6.pk)
        writer7 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer7.pk)
        writer8 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer8.pk)
        writer9 = writers_with_count_books_and_avg_mark_by_rating_of_books.get(pk=self.writer9.pk)

        self.assertEqual(writer1.avg_mark, 2.542)
        self.assertEqual(writer2.avg_mark, 1.333)
        self.assertEqual(writer3.avg_mark, 2.664)
        self.assertEqual(writer4.avg_mark, 2.908)
        self.assertEqual(writer5.avg_mark, 3.383)
        self.assertEqual(writer6.avg_mark, 0)
        self.assertEqual(writer7.avg_mark, 2.83)
        self.assertEqual(writer8.avg_mark, 2.748)
        self.assertEqual(writer9.avg_mark, 2.95)

        self.assertEqual(writer1.count_books, 4)
        self.assertEqual(writer2.count_books, 1)
        self.assertEqual(writer3.count_books, 6)
        self.assertEqual(writer4.count_books, 2)
        self.assertEqual(writer5.count_books, 3)
        self.assertEqual(writer6.count_books, 0)
        self.assertEqual(writer7.count_books, 5)
        self.assertEqual(writer8.count_books, 8)
        self.assertEqual(writer9.count_books, 7)
