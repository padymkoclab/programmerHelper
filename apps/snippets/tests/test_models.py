
from django.utils.text import slugify
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import accounts_factory, AccountFactory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory
from apps.favours.factories import FavourFactory
from apps.tags.models import Tag

from apps.snippets.factories import SnippetFactory
from apps.snippets.models import Snippet


class SnippetTest(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        accounts_factory(20)
        tags_factory(10)
        badges_factory()

    def setUp(self):
        self.snippet = SnippetFactory()

    def test_create_snippet(self):
        self.assertEqual(Snippet.objects.count(), 1)
        data = dict(
            title='Base class while testing, using for don`t DRY, but have many magic solutions for resolving problems.',
            lexer='Python 3',
            account=Account.objects.last(),
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
        tags_factory(10)
        web_links_factory(10)
        badges_factory()
        account_level_factory()
        accounts_factory(10)
        """,
        )
        snippet = Snippet(**data)
        snippet.full_clean()
        snippet.save()
        #
        snippet.tags.add(*Tag.objects.random_tags(4))
        for i in range(3):
            CommentFactory(content_object=snippet)
            OpinionFactory(content_object=snippet)
            FavourFactory(content_object=snippet)
        #
        self.assertEqual(snippet.title, data['title'])
        self.assertEqual(snippet.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(snippet.lexer, data['lexer'])
        self.assertEqual(snippet.account, data['account'])
        self.assertEqual(snippet.description, data['description'])
        self.assertEqual(snippet.code, data['code'])
        self.assertEqual(snippet.tags.count(), 4)
        self.assertEqual(snippet.comments.count(), 3)
        self.assertEqual(snippet.opinions.count(), 3)
        self.assertEqual(Snippet.objects.count(), 2)

    def test_unique_slug(self):
        same_title = 'Шаблонный тег для запуска ipdb c помощью django template language.'
        same_title_as_lower = same_title.lower()
        same_title_as_upper = same_title.upper()
        same_title_as_title = same_title.title()
        slug_same_title = slugify(same_title, allow_unicode=True)
        #
        snippet1 = SnippetFactory(title=same_title_as_lower)
        snippet2 = SnippetFactory(title=same_title_as_upper)
        snippet3 = SnippetFactory(title=same_title_as_title)
        #
        self.assertEqual(snippet1.title, same_title_as_lower)
        self.assertEqual(snippet1.slug, slug_same_title)
        self.assertEqual(snippet2.title, same_title_as_upper)
        self.assertEqual(snippet2.slug, slug_same_title + '-2')
        self.assertEqual(snippet3.title, same_title_as_title)
        self.assertEqual(snippet3.slug, slug_same_title + '-3')

    def test_update_snippet(self):
        account = AccountFactory()
        data_for_update = dict(
            title='Signal for keeping old value of the field, which may can using in future signals.',
            lexer='Python 3',
            account=account,
            description="""
This is may be the trivial approach for resolving keeping old value of the field.
May be who known better solutions for this problem, but if no. Using this snippet.
            """,
            code="""

OLD_ACCOUNT = None


@receiver(pre_save)
def signal_for_keeping_old_account(sender, instance, **kwargs):
    \"\"\"Write action in log.\"\"\"

    if sender in MODELS_WITH_FK_ACCOUNT:
        try:
            obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            if hasattr(instance, 'account'):
                account = instance.account
                old_account = obj.account
            global OLD_ACCOUNT
            if account != old_account:
                OLD_ACCOUNT = old_account
            else:
                OLD_ACCOUNT = None
        """,
        )
        self.snippet.title = data_for_update['title']
        self.snippet.lexer = data_for_update['lexer']
        self.snippet.account = data_for_update['account']
        self.snippet.description = data_for_update['description']
        self.snippet.code = data_for_update['code']
        self.snippet.full_clean()
        self.snippet.save()
        self.assertEqual(self.snippet.title, data_for_update['title'])
        self.assertEqual(self.snippet.slug, slugify(data_for_update['title'], allow_unicode=True))
        self.assertEqual(self.snippet.lexer, data_for_update['lexer'])
        self.assertEqual(self.snippet.account, data_for_update['account'])
        self.assertEqual(self.snippet.description, data_for_update['description'])
        self.assertEqual(self.snippet.code, data_for_update['code'])

    def test_delete_snippet(self):
        self.snippet.delete()

    def test_get_absolute_url(self):
        response = self.client.get(self.snippet.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_scope_of_the_snippet(self):
        self.snippet.opinions.clear()
        self.assertEqual(self.snippet.get_scope(), 0)
        random_accounts = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(10)
        choices_for_is_useful = [True, False, True, False, True, True, True, True, False, False]
        for couple in zip(random_accounts, choices_for_is_useful):
            self.snippet.opinions.create(account=couple[0], is_useful=couple[1])
        self.assertEqual(self.snippet.get_scope(), 2)
        self.snippet.opinions.clear()
        random_accounts = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(10)
        choices_for_is_useful = [False, False, True, False, True, True, True, True, False, False]
        for couple in zip(random_accounts, choices_for_is_useful):
            self.snippet.opinions.create(account=couple[0], is_useful=couple[1])
        self.assertEqual(self.snippet.get_scope(), 0)
        self.snippet.opinions.clear()
        random_accounts = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(10)
        choices_for_is_useful = [True, False, False, False, True, False, True, False, False, False]
        for couple in zip(random_accounts, choices_for_is_useful):
            self.snippet.opinions.create(account=couple[0], is_useful=couple[1])
        self.assertEqual(self.snippet.get_scope(), -4)

    def test_processing_tags(self):
        # restrict on max count tags and clear method
        pass

    def test_get_count_views(self):
        pass

    def test_show_users_given_bad_opinions(self):
        self.snippet.opinions.clear()
        self.assertFalse(self.snippet.show_users_given_bad_opinions())
        #
        account1, account2, account3, account4, account5 = Account.objects.random_accounts(5)
        self.snippet.opinions.create(account=account1, is_useful=True)
        self.snippet.opinions.create(account=account2, is_useful=False)
        self.snippet.opinions.create(account=account3, is_useful=False)
        self.snippet.opinions.create(account=account4, is_useful=True)
        self.snippet.opinions.create(account=account5, is_useful=False)
        #
        show_users_given_bad_opinions = self.snippet.show_users_given_bad_opinions()
        self.assertCountEqual([account2.username, account3.username, account5.username], show_users_given_bad_opinions)

    def test_show_users_given_good_opinions(self):
        self.snippet.opinions.clear()
        self.assertFalse(self.snippet.show_users_given_good_opinions())
        #
        account1, account2, account3, account4, account5 = Account.objects.random_accounts(5)
        self.snippet.opinions.create(account=account1, is_useful=False)
        self.snippet.opinions.create(account=account2, is_useful=False)
        self.snippet.opinions.create(account=account3, is_useful=True)
        self.snippet.opinions.create(account=account4, is_useful=False)
        self.snippet.opinions.create(account=account5, is_useful=True)
        #
        show_users_given_good_opinions = self.snippet.show_users_given_good_opinions()
        self.assertCountEqual([account3.username, account5.username], show_users_given_good_opinions)
