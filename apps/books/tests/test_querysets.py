
import statistics
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import factory_accounts, Factory_Account
from apps.tags.factories import factory_tags
from apps.badges.factories import factory_badges
from apps.web_links.factories import factory_web_links

from apps.books.factories import Factory_Book, Factory_Writter, factory_books, factory_writters
from apps.books.models import Book, Writter, NOW_YEAR


class BookQuerySetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        factory_tags(15)
        factory_web_links(15)
        factory_badges()
        factory_accounts(15)
        factory_books(15)

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
        """ """

        books_with_rating = Book.objects.books_with_rating()
        for book in books_with_rating.iterator():
            scopes = book.scopes.values_list('scope', flat=True)
            mean_scope = statistics.mean(scopes) if scopes else None
            self.assertEqual(mean_scope, book.rating)

    def test_books_with_count_tags_links_replies_and_rating(self):
        """ """

        books_with_count_tags_links_replies_and_rating = Book.objects.books_with_count_tags_links_replies_and_rating()
        for book in books_with_count_tags_links_replies_and_rating.iterator():
            self.assertEqual(book.tags.count(), book.count_tags)
            self.assertEqual(book.links.count(), book.count_links)
            self.assertEqual(book.replies.count(), book.count_replies)
            #
            scopes = book.scopes.values_list('scope', flat=True)
            mean_scope = statistics.mean(scopes) if scopes else None
            self.assertEqual(mean_scope, book.rating)

    def test_new_books(self):
        """This book published in this year or one year ago."""

        new_books = Book.objects.new_books()
        for book in Book.objects.iterator():
            if book.year_published in [NOW_YEAR, NOW_YEAR - 1]:
                self.assertIn(book, new_books)
