
from django.test import TestCase

from apps.app_solutions.factories import factory_categories_of_solutions_and_solutions
from apps.app_snippets.factories import factory_snippets
from apps.app_articles.factories import factory_articles
from apps.app_web_links.factories import factory_web_links
from apps.app_badges.factories import factory_badges
from apps.app_questions.factories import factory_questions_and_answers
from apps.app_books.factories import factory_books
from apps.app_accounts.factories import factory_accounts
from apps.app_books.models import Book
from apps.app_questions.models import Question
from apps.app_snippets.models import Snippet
from apps.app_articles.models import Article
from apps.app_solutions.models import Solution

from apps.app_tags.models import Tag
from apps.app_tags.factories import factory_tags


class Test_Tag(TestCase):

    @classmethod
    def setUpTestData(self):
        factory_web_links(15)
        factory_tags(20)
        factory_badges()
        factory_accounts(15)
        factory_categories_of_solutions_and_solutions(3)
        factory_snippets(5)
        factory_articles(4)
        factory_questions_and_answers(6, 3)
        factory_books(2)

    def setUp(self):
        self.tag = Tag.objects.first()

    def test_create_tag(self):
        count_tags = Tag.objects.count()
        tag = Tag(name='Linux-по-русски')
        tag.full_clean()
        tag.save()
        self.assertEqual(Tag.objects.count(), count_tags + 1)
        self.assertEqual(tag.name, 'Linux-по-русски')

    def test_update_tag(self):
        new_name = 'документация-jQuery'
        self.tag.name = new_name
        self.tag.save()
        self.assertEqual(self.tag.name, 'документация-jQuery')

    def test_delete_tag(self):
        count_tags = Tag.objects.count()
        self.tag.delete()
        self.assertEqual(Tag.objects.count(), count_tags - 1)

    def test_get_absolute_url_of_tag(self):
        response = self.client.get(self.tag.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_count_usage_of_tag_in_books(self):
        for obj in Book.objects.iterator():
            obj.tags.add(self.tag)
        self.assertEqual(self.tag.count_usage_in_books(), 2)

    def test_count_usage_of_tag_in_solutions(self):
        for obj in Solution.objects.iterator():
            obj.tags.add(self.tag)
        self.assertEqual(self.tag.count_usage_in_solutions(), 3)

    def test_count_usage_of_tag_in_articles(self):
        for obj in Article.objects.iterator():
            obj.tags.add(self.tag)
        self.assertEqual(self.tag.count_usage_in_articles(), 4)

    def test_count_usage_of_tag_in_questions(self):
        for obj in Question.objects.iterator():
            obj.tags.add(self.tag)
        self.assertEqual(self.tag.count_usage_in_questions(), 6)

    def test_count_usage_of_tag_in_snippets(self):
        for obj in Snippet.objects.iterator():
            obj.tags.add(self.tag)
        self.assertEqual(self.tag.count_usage_in_snippets(), 5)

    def test_total_count_usage_of_tag(self):
        for obj in Book.objects.iterator():
            obj.tags.add(self.tag)
        for obj in Snippet.objects.iterator():
            obj.tags.add(self.tag)
        for obj in Article.objects.iterator():
            obj.tags.add(self.tag)
        for obj in Solution.objects.iterator():
            obj.tags.add(self.tag)
        for obj in Question.objects.iterator():
            obj.tags.add(self.tag)
        self.assertEqual(self.tag.total_count_usage(), 20)
