
import datetime
import random
import re

from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory

from apps.books.models import Book, Writter
from apps.books.factories import books_factory, WritterFactory


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


class WritterManagerTest(TestCase):
    """
    Tests for custom manager of model Writter.
    """

    def test_mark_writter_dead_in_this_year(self):
        writter = WritterFactory(deathyear=None)
        self.assertIsNone(writter.deathyear)
        Writter.objects.mark_writter_dead_in_this_year(writter)
        self.assertEqual(writter.deathyear, datetime.datetime.now().year)

    def test_attempt_mark_writter_dead_in_this_year_if_he_dead_early(self):
        writter = WritterFactory(deathyear=datetime.datetime.now().year)
        self.assertIsNotNone(writter.deathyear)
        self.assertRaisesMessage(
            ValidationError, 'This writter already dead.', Writter.objects.mark_writter_dead_in_this_year, writter
        )
