
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import accounts_factory, AccountFactory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.scopes.factories import ScopeFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.utils import generate_text_certain_length

from apps.solutions.factories import SolutionFactory, SolutionCategoryFactory, solutions_categories_factory
from apps.solutions.models import Solution, SolutionCategory


class SolutionCategoryTest(TestCase):
    """
    TestCase for teting model 'SolutionCategory'.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        self.category = SolutionCategoryFactory(name='Вёрстка макета по готову шаблону')

    def test_create_category(self):
        data = dict(
            name='Русские переменные в коде Python',
            description=generate_text_certain_length(300),
        )
        category = SolutionCategory(**data)
        category.full_clean()
        category.save()
        self.assertEqual(category.name, data['name'])
        self.assertEqual(category.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(category.description, data['description'])

    def test_update_category(self):
        data = dict(
            name='Валидаторы Django',
            description=generate_text_certain_length(300),
        )
        #
        self.category.name = data['name']
        self.category.description = data['description']
        self.category.full_clean()
        self.category.save()
        #
        self.assertEqual(self.category.name, data['name'])
        self.assertEqual(self.category.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(self.category.description, data['description'])

    def test_delete_category(self):
        self.category.delete()

    def test_get_absolute_url(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_deny_using_point_in_end_name_of_category(self):
        category = SolutionCategory(name='Deploy django-project.', description=generate_text_certain_length(100))
        self.assertRaisesMessage(ValidationError, 'Don`t use point in end name of category of solution.', category.full_clean)
        category.name = category.name.rstrip('.')
        category.full_clean()
        category.save()

    def test_unique_slug(self):
        same_name = 'Тестирование Python с использованием Mock.'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify(same_name, allow_unicode=True)
        #
        category11 = SolutionCategoryFactory(name=same_name_as_lower)
        category12 = SolutionCategoryFactory(name=same_name_as_upper)
        category13 = SolutionCategoryFactory(name=same_name_as_title)
        #
        self.assertEqual(category11.name, same_name_as_lower)
        self.assertEqual(category11.slug, slug_same_name)
        self.assertEqual(category12.name, same_name_as_upper)
        self.assertEqual(category12.slug, slug_same_name + '-2')
        self.assertEqual(category13.name, same_name_as_title)
        self.assertEqual(category13.slug, slug_same_name + '-3')

    def test_total_scope(self):
        pass

    def test_latest_activity(self):
        pass


class SolutionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        solutions_categories_factory()

    def setUp(self):
        self.solution = SolutionFactory()

    def test_create_solution(self):
        data = dict(
            title='Создание PostgreSlq БД для django application.',
            body=generate_text_certain_length(1000),
            account=Account.objects.random_accounts(1),
            category=Solution.objects.first(),
        )
        solution = Solution(**data)
        solution.full_clean()
        solution.save()
        # adding tags and links
        solution.tags.add(*Tag.objects.random_tags(4))
        solution.links.add(*WebLink.objects.random_weblinks(3))
        # adding comments
        for i in range(4):
            CommentFactory(content_object=solution)
        # adding scopes
        for i in range(2):
            ScopeFactory(content_object=solution)
        #
        self.assertEqual(solution.title, data['title'])
        self.assertEqual(solution.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(solution.body, data['body'])
        self.assertEqual(solution.account, data['account'])
        self.assertEqual(solution.category, data['category'])
        self.assertEqual(solution.scopes.count(), 2)
        self.assertEqual(solution.tags.count(), 4)
        self.assertEqual(solution.links.count(), 3)
        self.assertEqual(solution.comments.count(), 4)

    def test_update_solution(self):
        new_category = SolutionCategoryFactory()
        new_account = AccountFactory()
        data = dict(
            title='Встраивание Python debuger (pdb) в Django Template Language(DTL).',
            body=generate_text_certain_length(1000),
            account=new_account,
            category=new_category,
        )
        self.solution.title = data['title']
        self.solution.body = data['body']
        self.solution.account = data['account']
        self.solution.category = data['category']
        self.solution.full_clean()
        self.solution.save()
        self.assertEqual(self.solution.title, data['title'])
        self.assertEqual(self.solution.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(self.solution.body, data['body'])
        self.assertEqual(self.solution.account, data['account'])
        self.assertEqual(self.solution.category, data['category'])

    def test_delete_solution(self):
        self.solution.delete()

    def test_unique_slug(self):
        same_title = 'Как просто и без трудностей сделать приятное рабочее окружение для программиста Python/JavaScript.'
        same_title_as_lower = same_title.lower()
        same_title_as_upper = same_title.upper()
        same_title_as_title = same_title.title()
        slug_same_title = slugify(same_title, allow_unicode=True)
        first_category = SolutionCategory.objects.first()
        last_category = SolutionCategory.objects.last()
        #
        solution11 = SolutionFactory(title=same_title_as_lower, category=first_category)
        solution12 = SolutionFactory(title=same_title_as_upper, category=first_category)
        solution13 = SolutionFactory(title=same_title_as_title, category=first_category)
        solution21 = SolutionFactory(title=same_title_as_lower, category=last_category)
        solution22 = SolutionFactory(title=same_title_as_upper, category=last_category)
        solution23 = SolutionFactory(title=same_title_as_title, category=last_category)
        #
        self.assertEqual(solution11.title, same_title_as_lower)
        self.assertEqual(solution11.slug, slug_same_title)
        self.assertEqual(solution12.title, same_title_as_upper)
        self.assertEqual(solution12.slug, slug_same_title + '-2')
        self.assertEqual(solution13.title, same_title_as_title)
        self.assertEqual(solution13.slug, slug_same_title + '-3')
        self.assertEqual(solution21.title, same_title_as_lower)
        self.assertEqual(solution21.slug, slug_same_title)
        self.assertEqual(solution22.title, same_title_as_upper)
        self.assertEqual(solution22.slug, slug_same_title + '-2')
        self.assertEqual(solution23.title, same_title_as_title)
        self.assertEqual(solution23.slug, slug_same_title + '-3')

    def test_get_absolute_url(self):
        response = self.client.get(self.solution.get_absolute_url())
        self.assertEqual(response.status_code, 200)

#     def test_get_rating(self):
#         self.solution.scopes.clear()
#         self.assertEqual(self.solution.get_rating(), .0)
#         ScopeFactory(content_object=self.solution, scope=2)
#         ScopeFactory(content_object=self.solution, scope=1)
#         ScopeFactory(content_object=self.solution, scope=0)
#         ScopeFactory(content_object=self.solution, scope=4)
#         ScopeFactory(content_object=self.solution, scope=5)
#         ScopeFactory(content_object=self.solution, scope=1)
#         ScopeFactory(content_object=self.solution, scope=4)
#         self.assertEqual(self.solution.get_rating(), 2.4286)

#     def test_get_volume(self):
#         all_items = list()
#         # length body and conclusion
#         len_body = len(self.solution.body)
#         len_conclusion = len(self.solution.conclusion)
#         # add lengths
#         all_items.extend([len_body, len_conclusion])
#         for category in self.solution.categories.iterator():
#             len_content = len(category.content)
#             all_items.append(len_content)
#         self.assertEqual(self.solution.get_volume(), sum(all_items))
#         # checkup with without categories
#         self.solution.categories.filter().delete()
#         self.assertEqual(self.solution.get_volume(), len_body + len_conclusion)

#     def test_tags_restrict(self):
#         pass

#     def test_links_restrict(self):
#         pass
