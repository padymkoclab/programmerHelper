
import unittest

from django.utils.text import slugify
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory
from apps.favours.factories import FavourFactory
from apps.tags.models import Tag
from mylabour.utils import generate_text_certain_length

from apps.snippets.factories import SnippetFactory
from apps.snippets.models import Snippet


class SnippetTest(TestCase):
    """
    Tests for model of snippets.
    """

    @classmethod
    def setUpTestData(cls):
        accounts_factory(20)
        tags_factory(10)
        badges_factory()

    def setUp(self):
        self.snippet = SnippetFactory()
        self.snippet.full_clean()

    def test_create_snippet(self):
        self.assertEqual(Snippet.objects.count(), 1)
        data = dict(
            title='Base class while testing, using for don`t DRY, but have many magic solutions for resolving problems.',
            lexer='javascript',
            account=Account.objects.active_accounts().random_accounts(),
            description=generate_text_certain_length(100),
            code=generate_text_certain_length(300),
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
        data_for_update = dict(
            title='Signal for keeping old value of the field, which may can using in future signals.',
            lexer='python3',
            account=Account.objects.exclude(pk=self.snippet.account.pk).active_accounts().random_accounts(),
            description=generate_text_certain_length(100),
            code=generate_text_certain_length(200),
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

    def test_get_mark_of_the_snippet(self):
        self.snippet.opinions.clear()
        self.assertEqual(self.snippet.get_mark(), 0)
        #
        random_accounts = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(10)
        choices_for_is_useful = [True, False, True, False, True, True, True, True, False, False]
        for couple in zip(random_accounts, choices_for_is_useful):
            self.snippet.opinions.create(account=couple[0], is_useful=couple[1])
        self.assertEqual(self.snippet.get_mark(), 2)
        #
        self.snippet.opinions.clear()
        random_accounts = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(10)
        choices_for_is_useful = [False, False, True, False, True, True, True, True, False, False]
        for couple in zip(random_accounts, choices_for_is_useful):
            self.snippet.opinions.create(account=couple[0], is_useful=couple[1])
        self.assertEqual(self.snippet.get_mark(), 0)
        #
        self.snippet.opinions.clear()
        random_accounts = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(10)
        choices_for_is_useful = [True, False, False, False, True, False, True, False, False, False]
        for couple in zip(random_accounts, choices_for_is_useful):
            self.snippet.opinions.create(account=couple[0], is_useful=couple[1])
        self.assertEqual(self.snippet.get_mark(), -4)

    @unittest.skip('Don`t made views counter.')
    def test_get_count_views(self):
        raise NotImplementedError

    def test_show_users_given_bad_opinions(self):
        self.snippet.opinions.clear()
        self.assertFalse(self.snippet.show_users_given_bad_opinions())
        #
        account1, account2, account3, account4, account5 = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(5)
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
        account1, account2, account3, account4, account5 = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(5)
        self.snippet.opinions.create(account=account1, is_useful=False)
        self.snippet.opinions.create(account=account2, is_useful=False)
        self.snippet.opinions.create(account=account3, is_useful=True)
        self.snippet.opinions.create(account=account4, is_useful=False)
        self.snippet.opinions.create(account=account5, is_useful=True)
        #
        show_users_given_good_opinions = self.snippet.show_users_given_good_opinions()
        self.assertCountEqual([account3.username, account5.username], show_users_given_good_opinions)

    def test_related_snippets_if_is_single_snippet(self):
        self.assertQuerysetEqual(self.snippet.related_snippets(), ())

    def test_related_snippets_by_only_lexer_and_not_snippets_with_same_lexer(self):
        self.snippet.tags.clear()
        SnippetFactory(lexer=self.snippet._select_another_lexer())
        SnippetFactory(lexer=self.snippet._select_another_lexer())
        SnippetFactory(lexer=self.snippet._select_another_lexer())
        self.assertQuerysetEqual(self.snippet.related_snippets(), ())

    def test_related_snippets_by_only_same_lexer(self):
        self.snippet.tags.clear()
        snippet1 = SnippetFactory(lexer=self.snippet.lexer)
        SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet2 = SnippetFactory(lexer=self.snippet.lexer)
        SnippetFactory(lexer=self.snippet._select_another_lexer())
        self.assertCountEqual(self.snippet.related_snippets(), (snippet1, snippet2))

    def test_related_snippets_by_only_tags_and_not_snippets_with_same_tags_at_all(self):
        snippet1 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet1.tags.clear()
        snippet2 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet2.tags.clear()
        snippet3 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet3.tags.clear()
        #
        self.snippet.tags.clear()
        self.assertQuerysetEqual(self.snippet.related_snippets(), ())
        #
        tags = Tag.objects.random_tags(5)
        self.snippet.tags.set(tags)
        snippet1.tags.set(Tag.objects.exclude(pk__in=tags))
        snippet2.tags.set(Tag.objects.exclude(pk__in=tags))
        snippet3.tags.set(Tag.objects.exclude(pk__in=tags))
        #
        self.assertQuerysetEqual(self.snippet.related_snippets(), ())

    def test_related_snippets_by_only_same_tags(self):
        snippet1 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet1.tags.clear()
        snippet2 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet2.tags.clear()
        snippet3 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet3.tags.clear()
        snippet4 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet4.tags.clear()
        snippet5 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet5.tags.clear()
        snippet6 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet6.tags.clear()
        #
        self.snippet.tags.clear()
        self.assertQuerysetEqual(self.snippet.related_snippets(), ())
        #
        tag1, tag2, tag3, tag4, tag5 = Tag.objects.random_tags(5)
        self.snippet.tags.set([tag1, tag2, tag3, tag4, tag5])
        # snippet1  #  0
        snippet2.tags.set([tag5])  # 1
        snippet3.tags.set([tag1, tag2, tag3])  # 3
        snippet4.tags.set([tag1, tag2, tag3, tag4, tag5])  # 5
        snippet5.tags.set([tag3, tag5])  # 2
        snippet6.tags.set([tag1, tag3, tag4, tag5])  # 4
        #
        self.assertQuerysetEqual(
            self.snippet.related_snippets(),
            map(repr, (snippet4, snippet6, snippet3, snippet5, snippet2))
        )

    def test_related_snippets_by_only_same_tags_with_partialy_overlap_tags(self):
        snippet1 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet1.tags.clear()
        snippet2 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet2.tags.clear()
        snippet3 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet3.tags.clear()
        snippet4 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet4.tags.clear()
        snippet5 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet5.tags.clear()
        snippet6 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet6.tags.clear()
        snippet7 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet7.tags.clear()
        snippet8 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet8.tags.clear()
        #
        self.snippet.tags.clear()
        self.assertQuerysetEqual(self.snippet.related_snippets(), ())
        #
        tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8 = Tag.objects.random_tags(8)
        self.snippet.tags.set([tag1, tag2, tag3, tag4, tag5])
        snippet1.tags.set([tag1, tag2, tag4, tag5])  # 4
        snippet2.tags.set([tag5])  # 1
        snippet3.tags.set([tag1, tag8, tag3])  # 2
        snippet4.tags.set([tag2, tag3, tag4, tag5, tag7])  # 4
        snippet5.tags.set([tag6, tag7, tag8])  # 0
        snippet6.tags.set([tag4, tag8])  # 1
        snippet7.tags.set([tag1, tag3, tag6, tag5])  # 3
        # snippet8  # 0
        related_snippets = self.snippet.related_snippets()
        #
        self.assertCountEqual(related_snippets[:2], (snippet1, snippet4))
        self.assertQuerysetEqual(related_snippets[2:4], map(repr, (snippet7, snippet3)))
        self.assertCountEqual(related_snippets[4:], (snippet2, snippet6))

    def test_related_snippets_with_same_lexer_and_same_tags(self):
        snippet1 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet1.tags.clear()
        snippet2 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet2.tags.clear()
        snippet3 = SnippetFactory(lexer=self.snippet.lexer)
        snippet3.tags.clear()
        snippet4 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet4.tags.clear()
        snippet5 = SnippetFactory(lexer=self.snippet.lexer)
        snippet5.tags.clear()
        snippet6 = SnippetFactory(lexer=self.snippet.lexer)
        snippet6.tags.clear()
        snippet7 = SnippetFactory(lexer=self.snippet.lexer)
        snippet7.tags.clear()
        snippet8 = SnippetFactory(lexer=self.snippet._select_another_lexer())
        snippet8.tags.clear()
        #
        self.snippet.tags.clear()
        tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8 = Tag.objects.random_tags(8)
        self.snippet.tags.set([tag1, tag2, tag3, tag4, tag5])
        #
        snippet1.tags.set([tag1, tag2, tag3, tag4, tag5])  # 5 + 0 = 5
        snippet2.tags.set([tag8])  # 0 + 0 = 0
        snippet3.tags.set([tag1, tag2, tag5, tag7, tag8])  # 3 + 1 = 4
        snippet4.tags.set([tag2, tag3])  # 2 + 0 = 2
        snippet5.tags.set([tag1, tag2, tag7])  # 2 + 1 = 3
        snippet6.tags.set([tag6, tag7, tag8])  # 0 + 1 = 1
        snippet7.tags.set([tag1, tag2, tag3, tag4, tag5])  # 5 + 1 = 6
        # snippet8  # 0
        #
        self.assertQuerysetEqual(
            self.snippet.related_snippets(),
            map(repr, (snippet7, snippet1, snippet3, snippet5, snippet4, snippet6)))

    def test_select_another_lexer(self):
        for i in range(100):
            self.assertNotEqual(self.snippet.lexer, self.snippet._select_another_lexer())

    def test_get_count_good_opinions_if_it_is_none(self):
        self.snippet.opinions.clear()
        self.assertFalse(self.snippet.get_count_good_opinions(), 0)

    def test_get_count_good_opinions_if_is(self):
        self.snippet.opinions.clear()
        #
        account1, account2, account3, account4, account5 = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(5)
        self.snippet.opinions.create(account=account1, is_useful=True)
        self.snippet.opinions.create(account=account2, is_useful=False)
        self.snippet.opinions.create(account=account3, is_useful=False)
        self.snippet.opinions.create(account=account4, is_useful=True)
        self.snippet.opinions.create(account=account5, is_useful=False)
        #
        self.assertEqual(self.snippet.get_count_good_opinions(), 2)

    def test_get_count_bad_opinions_if_it_is_none(self):
        self.snippet.opinions.clear()
        self.assertFalse(self.snippet.get_count_bad_opinions(), 0)

    def test_get_count_bad_opinions_if_is(self):
        self.snippet.opinions.clear()
        #
        account1, account2, account3, account4, account5 = Account.objects.exclude(pk=self.snippet.account.pk).random_accounts(5)
        self.snippet.opinions.create(account=account1, is_useful=True)
        self.snippet.opinions.create(account=account2, is_useful=False)
        self.snippet.opinions.create(account=account3, is_useful=False)
        self.snippet.opinions.create(account=account4, is_useful=True)
        self.snippet.opinions.create(account=account5, is_useful=False)
        #
        self.assertEqual(self.snippet.get_count_bad_opinions(), 3)
