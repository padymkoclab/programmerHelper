
from django.test import TestCase

from apps.solutions.factories import factory_categories_of_solutions_and_solutions
from apps.snippets.factories import factory_snippets
from apps.articles.factories import factory_articles
from apps.web_links.factories import factory_web_links
from apps.badges.factories import factory_badges
from apps.questions.factories import factory_questions_and_answers
from apps.books.factories import factory_books
from apps.accounts.factories import factory_accounts
from apps.books.models import Book
from apps.questions.models import Question
from apps.snippets.models import Snippet
from apps.articles.models import Article
from apps.solutions.models import Solution

from apps.tags.models import Tag
from apps.tags.factories import factory_tags


class Test_TagQuerySet(TestCase):

    @classmethod
    def setUpTestData(self):
        factory_web_links(10)
        factory_tags(15)
        factory_badges()
        factory_accounts(15)
        factory_categories_of_solutions_and_solutions(5)
        factory_snippets(5)
        factory_articles(5)
        factory_questions_and_answers(5, 0)
        factory_books(5)

    def setUp(self):
        self.tags = Tag.objects.all()

    def test_random_many_tags(self):
        random_tags = self.tags.random_tags(4)
        self.assertIsInstance(random_tags, (Tag.objects._queryset_class, ))
        intersection_tags = random_tags & self.tags.filter()
        self.assertEqual(len(intersection_tags), 4)

    def test_random_single_tag(self):
        random_tag = self.tags.random_tags(1)
        self.assertIsInstance(random_tag, (Tag, ))
        self.assertIn(random_tag, self.tags.filter())

    def test_tags_with_count_solutions(self):
        tag1, tag2, tag3, tag4 = self.tags.random_tags(4)
        tag1.solutions.clear()
        tag1.solutions.add(*Solution.objects.filter()[:3])
        tag2.solutions.clear()
        tag2.solutions.add(*Solution.objects.filter()[:5])
        tag3.solutions.clear()
        tag4.solutions.clear()
        tag4.solutions.add(*Solution.objects.filter()[:2])
        self.tags = self.tags.tags_with_count_solutions()
        self.assertEqual(self.tags.get(pk=tag1.pk).count_usage_in_solutions, 3)
        self.assertEqual(self.tags.get(pk=tag2.pk).count_usage_in_solutions, 5)
        self.assertEqual(self.tags.get(pk=tag3.pk).count_usage_in_solutions, 0)
        self.assertEqual(self.tags.get(pk=tag4.pk).count_usage_in_solutions, 2)

    def test_tags_with_count_articles(self):
        tag1, tag2, tag3, tag4 = self.tags.random_tags(4)
        tag1.articles.clear()
        tag1.articles.add(*Article.objects.filter()[:2])
        tag2.articles.clear()
        tag2.articles.add(*Article.objects.filter()[:4])
        tag3.articles.clear()
        self.tags = self.tags.tags_with_count_articles()
        self.assertEqual(self.tags.get(pk=tag1.pk).count_usage_in_articles, 2)
        self.assertEqual(self.tags.get(pk=tag2.pk).count_usage_in_articles, 4)
        self.assertEqual(self.tags.get(pk=tag3.pk).count_usage_in_articles, 0)

    def test_tags_with_count_snippets(self):
        tag1, tag2, tag3, tag4 = self.tags.random_tags(4)
        tag1.snippets.clear()
        tag1.snippets.add(*Snippet.objects.filter()[:1])
        tag2.snippets.clear()
        tag2.snippets.add(*Snippet.objects.filter()[:3])
        tag3.snippets.clear()
        tag3.snippets.add(*Snippet.objects.filter()[:5])
        tag4.snippets.clear()
        self.tags = self.tags.tags_with_count_snippets()
        self.assertEqual(self.tags.get(pk=tag1.pk).count_usage_in_snippets, 1)
        self.assertEqual(self.tags.get(pk=tag2.pk).count_usage_in_snippets, 3)
        self.assertEqual(self.tags.get(pk=tag3.pk).count_usage_in_snippets, 5)
        self.assertEqual(self.tags.get(pk=tag4.pk).count_usage_in_snippets, 0)

    def test_tags_with_count_books(self):
        tag1, tag2, tag3, tag4 = self.tags.random_tags(4)
        tag1.books.clear()
        tag1.books.add(*Book.objects.filter()[:1])
        tag2.books.clear()
        tag2.books.add(*Book.objects.filter()[:3])
        tag3.books.clear()
        tag3.books.add(*Book.objects.filter()[:5])
        tag4.books.clear()
        tag4.books.add(*Book.objects.filter()[:4])
        self.tags = self.tags.tags_with_count_books()
        self.assertEqual(self.tags.get(pk=tag1.pk).count_usage_in_books, 1)
        self.assertEqual(self.tags.get(pk=tag2.pk).count_usage_in_books, 3)
        self.assertEqual(self.tags.get(pk=tag3.pk).count_usage_in_books, 5)
        self.assertEqual(self.tags.get(pk=tag4.pk).count_usage_in_books, 4)

    def test_tags_with_count_questions(self):
        tag1, tag2, tag3, tag4 = self.tags.random_tags(4)
        tag1.questions.clear()
        tag1.questions.add(*Question.objects.filter()[:1])
        tag2.questions.clear()
        tag2.questions.add(*Question.objects.filter()[:3])
        tag3.questions.clear()
        tag3.questions.add(*Question.objects.filter()[:5])
        self.tags = self.tags.tags_with_count_questions()
        self.assertEqual(self.tags.get(pk=tag1.pk).count_usage_in_questions, 1)
        self.assertEqual(self.tags.get(pk=tag2.pk).count_usage_in_questions, 3)
        self.assertEqual(self.tags.get(pk=tag3.pk).count_usage_in_questions, 5)

    def test_tags_with_total_count_usage(self):
        tag1, tag2 = self.tags.random_tags(2)
        #
        tag1.books.clear()
        tag1.questions.clear()
        tag1.articles.clear()
        tag1.solutions.clear()
        tag1.snippets.clear()
        tag2.books.clear()
        tag2.questions.clear()
        tag2.articles.clear()
        tag2.solutions.clear()
        tag2.snippets.clear()
        #
        tag1.questions.add(*Question.objects.filter()[:1])
        tag1.books.add(*Book.objects.filter()[:2])
        tag1.snippets.add(*Snippet.objects.filter()[:3])
        tag1.solutions.add(*Solution.objects.filter()[:4])
        tag1.articles.add(*Article.objects.filter()[:5])
        tag2.questions.add(*Question.objects.filter()[:4])
        tag2.books.add(*Book.objects.filter()[:1])
        tag2.snippets.add(*Snippet.objects.filter()[:5])
        tag2.articles.add(*Article.objects.filter()[:3])
        #
        self.tags = self.tags.tags_with_total_count_usage()
        #
        self.assertEqual(self.tags.get(pk=tag1.pk).total_count_usage, 15)
        self.assertEqual(self.tags.get(pk=tag2.pk).total_count_usage, 13)
