
from django.test import TestCase

from apps.app_accounts.factories import factory_accounts, Factory_Account, factory_account_level
from apps.app_tags.factories import factory_tags

from apps.app_snippets.factories import Factory_Snippet
from apps.app_snippets.models import Snippet


class Test_Snippet(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        factory_account_level()
        factory_tags()

    def setUp(self):
        self.snippet = Factory_Snippet()

    def test_creating_snippet(self):
        self.assertEqual(Snippet.objects.count(), 0)
        author = Factory_Account()
        snippet = Snippet(
            title='Base class while testing, using for don`t DRY.',
            lexer='Python 3',
            author=author,
            description="""
Base class for using as base-abstract class for children classes.
It is simple realization previously populating the database for testing.
It is became possible by using method setUpTestData().
            """,
            code="""
class BaseTestClass_for_prepopulated_data(TestCase):
    \"\"\"

    \"\"\"

    @classmethod
    def setUpTestData(cls):
        factory_tags(10)
        factory_web_links(10)
        factory_badges()
        factory_account_level()
        factory_accounts(10)
        """,
        )
        snippet.full_clean()
        snippet.save()
        # snippet.tags.add(*Tag.objects.)
        self.assertEual(Snippet.objects.count(), 1)
