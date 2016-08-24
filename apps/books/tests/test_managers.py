
import datetime
import random
import re

from django.test import TestCase
from django.core.exceptions import ValidationError

from psycopg2.extras import NumericRange

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory

from apps.books.models import Book, Writer
from apps.books.factories import books_factory, WriterFactory


class BookManagerTest(TestCase):
    """
    Tests for custom manager of model Book.
    """

    def setUp(self):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        books_factory(15)

    def test_made_all_books_as_wrote_on_english(self):
        # made all books as non english
        non_enlish_languages = tuple(filter(lambda x: not re.match('^en-?', x[0]), Book.LANGUAGES))
        for book in Book.objects.iterator():
            book.language = random.choice(non_enlish_languages)[0]
            book.full_clean()
            book.save()
        # test what all books is wrote on non english
        self.assertEqual(Book.objects.books_wrote_english().count(), 0)
        # made all books as english
        Book.objects.made_all_books_as_wrote_on_english()
        # test what all books is wrote on english
        self.assertCountEqual(Book.objects.books_wrote_english(), Book.objects.all())


class WriterManagerTest(TestCase):
    """
    Tests for custom manager of model Writer.
    """

    def test_mark_writer_dead_in_this_year(self):
        writer = WriterFactory(years_life=NumericRange(1990, None))
        self.assertIsNone(writer.years_life.upper)
        Writer.objects.mark_writer_dead_in_this_year(writer)
        self.assertEqual(writer.years_life.upper, datetime.datetime.now().year)

    def test_attempt_mark_writer_dead_in_this_year_if_he_dead_early(self):
        writer = WriterFactory(years_life=NumericRange(1930, datetime.datetime.now().year))
        self.assertIsNotNone(writer.years_life.upper)
        self.assertRaisesMessage(
            ValidationError, 'This writer already dead.', Writer.objects.mark_writer_dead_in_this_year, writer
        )
