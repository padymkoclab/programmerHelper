
from django.test import TestCase

from apps.app_accounts.models import Account
from apps.app_accounts.factories import factory_accounts
from apps.app_tags.factories import factory_tags
from apps.app_badges.factories import factory_badges
from apps.app_tags.models import Tag

from apps.app_snippets.factories import factory_snippets
from apps.app_snippets.models import Snippet


class Test_SnippetQuerySet(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        #
        factory_accounts(17)
        factory_tags(10)
        factory_badges()
        factory_snippets(5)
        # change snippets for testing
        cls.snippet1, cls.snippet2, cls.snippet3, cls.snippet4, cls.snippet5 = Snippet.objects.all()
        # clear all tags, opinions, comments in each of the snippet
        for snippet in [cls.snippet1, cls.snippet2, cls.snippet3, cls.snippet4, cls.snippet5]:
            snippet.tags.clear()
            snippet.opinions.clear()
            snippet.comments.clear()
        # add tags
        cls.snippet1.tags.add(*Tag.objects.random_tags(4))
        cls.snippet2.tags.add(*Tag.objects.random_tags(5))
        cls.snippet3.tags.add(*Tag.objects.random_tags(2))
        cls.snippet4.tags.add(*Tag.objects.random_tags(3))
        cls.snippet5.tags.add(Tag.objects.random_tags(1))
        # add opinions
        accounts = Account.objects.exclude(pk__in=Snippet.objects.values('account'))
        opinions_for_snippet1 = [1, 0, 0, 0, 0, 0, 1, 0, 1, 0]
        opinions_for_snippet2 = [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
        opinions_for_snippet3 = [1, 0, 1, 0, 0, 1, 1, 1]
        opinions_for_snippet4 = [0, 1, 1]
        opinions_for_snippet5 = [1, 1, 1, 0, 1, 0, 0, 0]
        for couple in zip(accounts, opinions_for_snippet1):
            cls.snippet1.opinions.create(account=couple[0], is_useful=couple[1])
        for couple in zip(accounts, opinions_for_snippet2):
            cls.snippet2.opinions.create(account=couple[0], is_useful=couple[1])
        for couple in zip(accounts, opinions_for_snippet3):
            cls.snippet3.opinions.create(account=couple[0], is_useful=couple[1])
        for couple in zip(accounts, opinions_for_snippet4):
            cls.snippet4.opinions.create(account=couple[0], is_useful=couple[1])
        for couple in zip(accounts, opinions_for_snippet5):
            cls.snippet5.opinions.create(account=couple[0], is_useful=couple[1])
        # add comments
        cls.snippet1.comments.create(account=Account.objects.random_accounts(1), text_comment='Hi, it is very nice snippet.')
        cls.snippet1.comments.create(account=Account.objects.random_accounts(1), text_comment='Bad snippet.')
        cls.snippet1.comments.create(account=Account.objects.random_accounts(1), text_comment='Interesting snippet.')
        cls.snippet2.comments.create(account=Account.objects.random_accounts(1), text_comment='Nice snippet.')
        cls.snippet2.comments.create(account=Account.objects.random_accounts(1), text_comment='This is charm.')
        cls.snippet2.comments.create(account=Account.objects.random_accounts(1), text_comment='No. This is awesome snipet.')
        cls.snippet2.comments.create(account=Account.objects.random_accounts(1), text_comment='Thank`s author`s of the snippet.')
        cls.snippet3.comments.create(account=Account.objects.random_accounts(1), text_comment='Simple snippet.')
        cls.snippet4.comments.create(account=Account.objects.random_accounts(1), text_comment='Stupid snippet.')
        cls.snippet4.comments.create(account=Account.objects.random_accounts(1), text_comment='Amazing snippet.')
        cls.snippet5.comments.create(account=Account.objects.random_accounts(1), text_comment='Non insteresting snippet.')

    def test_snippets_with_scopes(self):
        snippets_with_scopes = Snippet.objects.snippets_with_scopes()
        self.assertEqual(snippets_with_scopes.get(pk=self.snippet1.pk).scope, -4)
        self.assertEqual(snippets_with_scopes.get(pk=self.snippet2.pk).scope, 6)
        self.assertEqual(snippets_with_scopes.get(pk=self.snippet3.pk).scope, 2)
        self.assertEqual(snippets_with_scopes.get(pk=self.snippet4.pk).scope, 1)
        self.assertEqual(snippets_with_scopes.get(pk=self.snippet5.pk).scope, 0)

    def test_snippets_with_count_tags(self):
        snippets_with_count_tags = Snippet.objects.snippets_with_count_tags()
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet1.pk).count_tags, 4)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet2.pk).count_tags, 5)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet3.pk).count_tags, 2)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet4.pk).count_tags, 3)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet5.pk).count_tags, 1)

    def test_snippets_with_count_good_opinions(self):
        snippets_with_count_good_opinions = Snippet.objects.snippets_with_count_good_opinions()
        self.assertEqual(snippets_with_count_good_opinions.get(pk=self.snippet1.pk).count_good_opinions, 3)
        self.assertEqual(snippets_with_count_good_opinions.get(pk=self.snippet2.pk).count_good_opinions, 9)
        self.assertEqual(snippets_with_count_good_opinions.get(pk=self.snippet3.pk).count_good_opinions, 5)
        self.assertEqual(snippets_with_count_good_opinions.get(pk=self.snippet4.pk).count_good_opinions, 2)
        self.assertEqual(snippets_with_count_good_opinions.get(pk=self.snippet5.pk).count_good_opinions, 4)

    def test_snippets_with_count_bad_opinions(self):
        snippets_with_count_bad_opinions = Snippet.objects.snippets_with_count_bad_opinions()
        self.assertEqual(snippets_with_count_bad_opinions.get(pk=self.snippet1.pk).count_bad_opinions, 7)
        self.assertEqual(snippets_with_count_bad_opinions.get(pk=self.snippet2.pk).count_bad_opinions, 3)
        self.assertEqual(snippets_with_count_bad_opinions.get(pk=self.snippet3.pk).count_bad_opinions, 3)
        self.assertEqual(snippets_with_count_bad_opinions.get(pk=self.snippet4.pk).count_bad_opinions, 1)
        self.assertEqual(snippets_with_count_bad_opinions.get(pk=self.snippet5.pk).count_bad_opinions, 4)

    def test_snippets_with_count_opinions(self):
        snippets_with_count_opinions = Snippet.objects.snippets_with_count_opinions()
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet1.pk).count_opinions, 10)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet2.pk).count_opinions, 12)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet3.pk).count_opinions, 8)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet4.pk).count_opinions, 3)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet5.pk).count_opinions, 8)

    def test_snippets_with_count_comments(self):
        snippets_with_count_comments = Snippet.objects.snippets_with_count_comments()
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet1.pk).count_comments, 3)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet2.pk).count_comments, 4)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet3.pk).count_comments, 1)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet4.pk).count_comments, 2)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet5.pk).count_comments, 1)

    def test_snippets_by_scopes_without_required_arguments(self):
        self.assertRaisesMessage(
            TypeError,
            'Missing 1 required argument: "min_scope" or "max_scope".',
            Snippet.objects.snippets_by_scopes,
        )

    def test_snippets_by_scopes_with_only_max_scope(self):
        snippets = Snippet.objects.snippets_by_scopes(max_scope=1)
        self.assertCountEqual(snippets, [self.snippet1, self.snippet4, self.snippet5])

    def test_snippets_by_scopes_with_only_min_scope(self):
        snippets = Snippet.objects.snippets_by_scopes(min_scope=1)
        self.assertCountEqual(snippets, [self.snippet2, self.snippet4, self.snippet3])

    def test_snippets_by_scopes_with_min_and_max_scope(self):
        snippets = Snippet.objects.snippets_by_scopes(min_scope=-1, max_scope=1)
        self.assertCountEqual(snippets, [self.snippet4, self.snippet5])

    def test_snippets_with_count_tags_opinions_comments_scopes_and_count_good_or_bad_opinions(self):
        snippets = Snippet.objects.snippets_with_count_tags_opinions_comments_scopes_and_count_good_or_bad_opinions()
        #
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_bad_opinions, 7)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_comments, 3)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_good_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_opinions, 10)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_tags, 4)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).scope, -4)
        #
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_bad_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_comments, 4)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_good_opinions, 9)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_opinions, 12)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_tags, 5)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).scope, 6)
        #
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_bad_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_comments, 1)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_good_opinions, 5)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_opinions, 8)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_tags, 2)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).scope, 2)
        #
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_bad_opinions, 1)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_comments, 2)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_good_opinions, 2)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_tags, 3)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).scope, 1)
        #
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_bad_opinions, 4)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_comments, 1)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_good_opinions, 4)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_opinions, 8)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_tags, 1)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).scope, 0)
