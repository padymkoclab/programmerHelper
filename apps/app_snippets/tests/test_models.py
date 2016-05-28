
from django.test import TestCase

from apps.app_accounts.models import Account
from apps.app_accounts.factories import factory_accounts, Factory_Account
from apps.app_tags.factories import factory_tags
from apps.app_badges.factories import factory_badges
from apps.app_comments.factories import Factory_Comment
from apps.app_opinions.factories import Factory_Opinion
from apps.app_favours.factories import Factory_Favour
from apps.app_tags.models import Tag

from apps.app_snippets.factories import Factory_Snippet
from apps.app_snippets.models import Snippet


class Test_Snippet(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        factory_accounts(15)
        factory_tags(10)
        factory_badges()

    def setUp(self):
        self.snippet = Factory_Snippet()

    def test_create_snippet(self):
        self.assertEqual(Snippet.objects.count(), 1)
        account = Factory_Account()
        data = dict(
            title='Base class while testing, using for don`t DRY.',
            lexer='Python 3',
            account=account,
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
        snippet = Snippet(**data)
        snippet.full_clean()
        snippet.save()
        self.assertEqual(Snippet.objects.count(), 2)
        self.assertEqual(snippet.title, data['title'])
        self.assertEqual(snippet.lexer, data['lexer'])
        self.assertEqual(snippet.account, data['account'])
        self.assertEqual(snippet.description, data['description'])
        self.assertEqual(snippet.code, data['code'])
        #
        snippet.tags.add(*Tag.objects.random_tags(4))
        for i in range(3):
            Factory_Comment(content_object=snippet)
            Factory_Opinion(content_object=snippet)
            Factory_Favour(content_object=snippet)
        self.assertEqual(snippet.tags.count(), 4)
        self.assertEqual(snippet.comments.count(), 3)
        self.assertEqual(snippet.opinions.count(), 3)

    def test_update_snippet(self):
        account = Factory_Account()
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
        self.snippet.full_clean(exclude=['slug'])
        self.snippet.save()
        self.assertEqual(self.snippet.title, data_for_update['title'])
        self.assertEqual(self.snippet.lexer, data_for_update['lexer'])
        self.assertEqual(self.snippet.account, data_for_update['account'])
        self.assertEqual(self.snippet.description, data_for_update['description'])
        self.assertEqual(self.snippet.code, data_for_update['code'])

    def test_delete_snippet(self):
        self.assertEqual(Snippet.objects.count(), 1)
        self.snippet.delete()
        self.assertEqual(Snippet.objects.count(), 0)

    def test_get_absolute_url(self):
        response = self.client.get(self.snippet.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_scope_of_the_snippet(self):
        self.snippet.opinions.clear()
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

    def test_get_count_views(self):
        pass
