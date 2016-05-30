
import datetime

from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import factory_accounts, Factory_Account
from apps.tags.factories import factory_tags
from apps.badges.factories import factory_badges
from apps.web_links.factories import factory_web_links
from apps.replies.factories import Factory_Reply
from apps.scopes.factories import Factory_Scope
from apps.tags.models import Tag
from apps.web_links.models import WebLink

from apps.books.factories import Factory_Book, Factory_Writter, factory_books
from apps.books.models import Book, Writter


class BookTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        factory_tags(30)
        factory_web_links(30)
        factory_badges()
        factory_accounts(15)

    def test_create_weblink(self):
        pass

    def test_update_weblink(self):
        pass
