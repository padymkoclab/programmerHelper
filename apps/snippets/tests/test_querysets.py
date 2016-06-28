
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.tags.models import Tag

from apps.snippets.factories import snippets_factory
from apps.snippets.models import Snippet


class SnippetQuerySetTest(TestCase):
    """
    Tests for snippets`s queryset.
    """

    @classmethod
    def setUpTestData(cls):
        #
        accounts_factory(25)
        tags_factory(10)
        badges_factory()
        snippets_factory(7)
        # change snippets for testing
        cls.snippet1, cls.snippet2, cls.snippet3, cls.snippet4, cls.snippet5, cls.snippet6, cls.snippet7 = Snippet.objects.all()
        # clear all tags, opinions, comments in each of the snippet
        for snippet in [cls.snippet1, cls.snippet2, cls.snippet3, cls.snippet4, cls.snippet5, cls.snippet6, cls.snippet7]:
            snippet.tags.clear()
            snippet.opinions.clear()
            snippet.comments.clear()
            snippet.favours.clear()
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
        opinions_for_snippet4 = [1, 1, 1]
        opinions_for_snippet5 = [1, 1, 1, 0, 1, 0, 0, 0]
        opinions_for_snippet6 = [0, 0, 0]
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
        for couple in zip(accounts, opinions_for_snippet6):
            cls.snippet6.opinions.create(account=couple[0], is_useful=couple[1])
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
        # add favours
        favours_for_snippet1 = [1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0]
        favours_for_snippet2 = [1, 1, 0, 1, 0]
        favours_for_snippet3 = [1, 0, 0, 0, 0, 0, 0, 1]
        favours_for_snippet4 = [1, 1]
        favours_for_snippet5 = [1, 0]
        favours_for_snippet6 = [0, 0, 0, 0]
        for couple in zip(accounts, favours_for_snippet1):
            cls.snippet1.favours.create(account=couple[0], is_favour=couple[1])
        for couple in zip(accounts, favours_for_snippet2):
            cls.snippet2.favours.create(account=couple[0], is_favour=couple[1])
        for couple in zip(accounts, favours_for_snippet3):
            cls.snippet3.favours.create(account=couple[0], is_favour=couple[1])
        for couple in zip(accounts, favours_for_snippet4):
            cls.snippet4.favours.create(account=couple[0], is_favour=couple[1])
        for couple in zip(accounts, favours_for_snippet5):
            cls.snippet5.favours.create(account=couple[0], is_favour=couple[1])
        for couple in zip(accounts, favours_for_snippet6):
            cls.snippet6.favours.create(account=couple[0], is_favour=couple[1])

    def test_objects_with_marks(self):
        objects_with_marks = Snippet.objects.objects_with_marks()
        self.assertEqual(objects_with_marks.get(pk=self.snippet1.pk).mark, -4)
        self.assertEqual(objects_with_marks.get(pk=self.snippet2.pk).mark, 6)
        self.assertEqual(objects_with_marks.get(pk=self.snippet3.pk).mark, 2)
        self.assertEqual(objects_with_marks.get(pk=self.snippet4.pk).mark, 3)
        self.assertEqual(objects_with_marks.get(pk=self.snippet5.pk).mark, 0)
        self.assertEqual(objects_with_marks.get(pk=self.snippet6.pk).mark, -3)
        self.assertEqual(objects_with_marks.get(pk=self.snippet7.pk).mark, 0)

    def test_snippets_with_count_tags(self):
        snippets_with_count_tags = Snippet.objects.snippets_with_count_tags()
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet1.pk).count_tags, 4)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet2.pk).count_tags, 5)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet3.pk).count_tags, 2)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet4.pk).count_tags, 3)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet5.pk).count_tags, 1)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet6.pk).count_tags, 0)
        self.assertEqual(snippets_with_count_tags.get(pk=self.snippet7.pk).count_tags, 0)

    def test_snippets_with_count_opinions(self):
        snippets_with_count_opinions = Snippet.objects.snippets_with_count_opinions()
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet1.pk).count_opinions, 10)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet2.pk).count_opinions, 12)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet3.pk).count_opinions, 8)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet4.pk).count_opinions, 3)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet5.pk).count_opinions, 8)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet6.pk).count_opinions, 3)
        self.assertEqual(snippets_with_count_opinions.get(pk=self.snippet7.pk).count_opinions, 0)

    def test_snippets_with_count_comments(self):
        snippets_with_count_comments = Snippet.objects.snippets_with_count_comments()
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet1.pk).count_comments, 3)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet2.pk).count_comments, 4)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet3.pk).count_comments, 1)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet4.pk).count_comments, 2)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet5.pk).count_comments, 1)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet6.pk).count_comments, 0)
        self.assertEqual(snippets_with_count_comments.get(pk=self.snippet7.pk).count_comments, 0)

    def test_snippets_with_count_favours(self):
        snippets_with_count_favours = Snippet.objects.snippets_with_count_favours()
        self.assertEqual(snippets_with_count_favours.get(pk=self.snippet1.pk).count_favours, 15)
        self.assertEqual(snippets_with_count_favours.get(pk=self.snippet2.pk).count_favours, 5)
        self.assertEqual(snippets_with_count_favours.get(pk=self.snippet3.pk).count_favours, 8)
        self.assertEqual(snippets_with_count_favours.get(pk=self.snippet4.pk).count_favours, 2)
        self.assertEqual(snippets_with_count_favours.get(pk=self.snippet5.pk).count_favours, 2)
        self.assertEqual(snippets_with_count_favours.get(pk=self.snippet6.pk).count_favours, 4)
        self.assertEqual(snippets_with_count_favours.get(pk=self.snippet7.pk).count_favours, 0)

    def test_snippets_with_count_like_favours(self):
        snippets_with_count_like_favours = Snippet.objects.snippets_with_count_like_favours()
        self.assertEqual(snippets_with_count_like_favours.get(pk=self.snippet1.pk).count_like_favours, 9)
        self.assertEqual(snippets_with_count_like_favours.get(pk=self.snippet2.pk).count_like_favours, 3)
        self.assertEqual(snippets_with_count_like_favours.get(pk=self.snippet3.pk).count_like_favours, 2)
        self.assertEqual(snippets_with_count_like_favours.get(pk=self.snippet4.pk).count_like_favours, 2)
        self.assertEqual(snippets_with_count_like_favours.get(pk=self.snippet5.pk).count_like_favours, 1)
        self.assertEqual(snippets_with_count_like_favours.get(pk=self.snippet6.pk).count_like_favours, 0)
        self.assertEqual(snippets_with_count_like_favours.get(pk=self.snippet7.pk).count_like_favours, 0)

    def test_snippets_with_count_dislike_favours(self):
        snippets_with_count_dislike_favours = Snippet.objects.snippets_with_count_dislike_favours()
        self.assertEqual(snippets_with_count_dislike_favours.get(pk=self.snippet1.pk).count_dislike_favours, 6)
        self.assertEqual(snippets_with_count_dislike_favours.get(pk=self.snippet2.pk).count_dislike_favours, 2)
        self.assertEqual(snippets_with_count_dislike_favours.get(pk=self.snippet3.pk).count_dislike_favours, 6)
        self.assertEqual(snippets_with_count_dislike_favours.get(pk=self.snippet4.pk).count_dislike_favours, 0)
        self.assertEqual(snippets_with_count_dislike_favours.get(pk=self.snippet5.pk).count_dislike_favours, 1)
        self.assertEqual(snippets_with_count_dislike_favours.get(pk=self.snippet6.pk).count_dislike_favours, 4)
        self.assertEqual(snippets_with_count_dislike_favours.get(pk=self.snippet7.pk).count_dislike_favours, 0)

    def test_snippets_by_marks_without_required_arguments(self):
        self.assertRaisesMessage(
            TypeError,
            'Missing 1 required argument: "min_mark" or "max_mark".',
            Snippet.objects.snippets_by_marks,
        )

    def test_snippets_by_marks_with_only_max_mark(self):
        snippets = Snippet.objects.snippets_by_marks(max_mark=1)
        self.assertCountEqual(snippets, [self.snippet1, self.snippet5, self.snippet6, self.snippet7])

    def test_snippets_by_marks_with_only_min_mark(self):
        snippets = Snippet.objects.snippets_by_marks(min_mark=1)
        self.assertCountEqual(snippets, [self.snippet2, self.snippet4, self.snippet3])

    def test_snippets_by_marks_with_min_and_max_mark(self):
        snippets = Snippet.objects.snippets_by_marks(min_mark=-1, max_mark=1)
        self.assertCountEqual(snippets, [self.snippet5, self.snippet7])

    def test_snippets_with_total_counters_on_related_fields(self):
        snippets = Snippet.objects.snippets_with_total_counters_on_related_fields()
        #
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_comments, 3)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_opinions, 10)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_tags, 4)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).mark, -4)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_good_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_bad_opinions, 7)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_favours, 15)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_like_favours, 9)
        self.assertEqual(snippets.get(pk=self.snippet1.pk).count_dislike_favours, 6)
        #
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_comments, 4)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_opinions, 12)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_tags, 5)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).mark, 6)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_good_opinions, 9)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_bad_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_favours, 5)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_like_favours, 3)
        self.assertEqual(snippets.get(pk=self.snippet2.pk).count_dislike_favours, 2)
        #
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_comments, 1)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_opinions, 8)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_tags, 2)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).mark, 2)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_good_opinions, 5)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_bad_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_favours, 8)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_like_favours, 2)
        self.assertEqual(snippets.get(pk=self.snippet3.pk).count_dislike_favours, 6)
        #
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_comments, 2)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_tags, 3)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).mark, 1)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_good_opinions, 2)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_bad_opinions, 1)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_favours, 2)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_like_favours, 2)
        self.assertEqual(snippets.get(pk=self.snippet4.pk).count_dislike_favours, 0)
        #
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_comments, 1)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_opinions, 8)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_tags, 1)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).mark, 0)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_good_opinions, 4)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_bad_opinions, 4)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_favours, 2)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_like_favours, 1)
        self.assertEqual(snippets.get(pk=self.snippet5.pk).count_dislike_favours, 1)
        #
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_comments, 0)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_tags, 0)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).mark, -3)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_good_opinions, 0)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_bad_opinions, 3)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_favours, 4)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_like_favours, 0)
        self.assertEqual(snippets.get(pk=self.snippet6.pk).count_dislike_favours, 4)
        #
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_comments, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_opinions, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_tags, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).mark, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_good_opinions, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_bad_opinions, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_favours, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_like_favours, 0)
        self.assertEqual(snippets.get(pk=self.snippet7.pk).count_dislike_favours, 0)
