
import unittest

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.factories import accounts_factory, AccountFactory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from utils.django.utils import generate_text_by_min_length

from apps.solutions.factories import SolutionFactory, SolutionCategoryFactory, solutions_categories_factory
from apps.solutions.models import Solution, SolutionCategory


class SolutionCategoryTest(TestCase):
    """
    Tests for categories of solutions.
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
            description=generate_text_by_min_length(300),
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
            description=generate_text_by_min_length(300),
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

    @unittest.skip('Not implemented')
    def test_get_total_scope(self):
        self.category.solutions.filter().delete()
        self.assertEqual(self.category.get_total_scope(), .0)
        #
        solution = SolutionFactory(category=self.category)
        solution.opinions.clear()
        self.assertEqual(self.category.get_total_scope(), .0)
        OpinionFactory(content_object=solution, is_useful=True)
        self.assertEqual(self.category.get_total_scope(), 1)

    def test_get_latest_activity(self):
        # create new category
        category = SolutionCategoryFactory()

        # without solutions
        self.assertEqual(category.get_latest_activity(), category.date_modified)

        # change date_modified but still without solutions
        category.save()
        self.assertEqual(category.get_latest_activity(), category.date_modified)

        # added first solution
        solution1 = SolutionFactory(category=category)
        self.assertEqual(category.get_latest_activity(), solution1.date_modified)

        # added second solution
        solution2 = SolutionFactory(category=category)
        self.assertEqual(category.get_latest_activity(), solution2.date_modified)

        # added third solution
        solution3 = SolutionFactory(category=category)
        self.assertEqual(category.get_latest_activity(), solution3.date_modified)

        # change first solution
        solution1.save()
        self.assertEqual(category.get_latest_activity(), solution1.date_modified)

        # change third solution
        solution3.save()
        self.assertEqual(category.get_latest_activity(), solution3.date_modified)

        # change category
        category.save()
        self.assertEqual(category.get_latest_activity(), category.date_modified)

        # change second solution
        solution2.save()
        self.assertEqual(category.get_latest_activity(), solution2.date_modified)

        # clear all solutions
        category.solutions.filter().delete()
        self.assertEqual(category.get_latest_activity(), category.date_modified)

    @unittest.skip('Not implemented')
    def test_categories_with_count_solutions_total_scope_and_latest_activity(self):
        pass


class SolutionTest(TestCase):
    """
    Test for solutions.
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        solutions_categories_factory()

    def setUp(self):
        self.solution = SolutionFactory()
        self.solution.full_clean()

    def test_create_solution(self):
        data = dict(
            title='Создание PostgreSlq БД для django application.',
            body=generate_text_by_min_length(1000),
            account=Account.objects.active_accounts().random_accounts(1),
            category=SolutionCategory.objects.first(),
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
        # adding opinions
        for i in range(2):
            OpinionFactory(content_object=solution)
        #
        self.assertEqual(solution.title, data['title'])
        self.assertEqual(solution.slug, slugify(data['title'], allow_unicode=True))
        self.assertEqual(solution.body, data['body'])
        self.assertEqual(solution.account, data['account'])
        self.assertEqual(solution.category, data['category'])
        self.assertEqual(solution.opinions.count(), 2)
        self.assertEqual(solution.tags.count(), 4)
        self.assertEqual(solution.links.count(), 3)
        self.assertEqual(solution.comments.count(), 4)

    def test_update_solution(self):
        new_category = SolutionCategoryFactory()
        new_account = AccountFactory(is_active=True)
        data = dict(
            title='Встраивание Python debuger (pdb) в Django Template Language(DTL).',
            body=generate_text_by_min_length(1000),
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

    def test_get_admin_page_url(self):
        raise NotImplementedError

    def test_change_unique_error_message(self):
        solution = Solution(title=self.solution.title, category=self.solution.category)
        self.assertRaisesMessage(
            ValidationError,
            'Solution with this title already exists in this category of solutions.',
            solution.full_clean
        )

    @unittest.skip('Not implemented')
    def test_get_scope(self):
        #
        self.solution.opinions.clear()
        self.assertEqual(self.solution.get_scope(), '0')
        #
        OpinionFactory(content_object=self.solution, is_useful=True)
        self.assertEqual(self.solution.get_scope(), '+1')
        #
        OpinionFactory(content_object=self.solution, is_useful=False)
        OpinionFactory(content_object=self.solution, is_useful=False)
        self.assertEqual(self.solution.get_scope(), '-1')
        #
        OpinionFactory(content_object=self.solution, is_useful=True)
        OpinionFactory(content_object=self.solution, is_useful=True)
        OpinionFactory(content_object=self.solution, is_useful=True)
        OpinionFactory(content_object=self.solution, is_useful=True)
        self.assertEqual(self.solution.get_scope(), '+3')
        #
        self.solution.opinions.clear()
        self.assertEqual(self.solution.get_scope(), '0')

    def test_get_quality(self):
        # get 7 accounts (exclude author of solution)
        accounts = Account.objects.exclude(pk=self.solution.account.pk).active_accounts().random_accounts(7)
        # scope 0
        self.solution.opinions.clear()
        self.assertEqual(self.solution.get_quality(), 'Vague')
        # scope +1
        opinion0 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[0])
        self.assertEqual(self.solution.get_quality(), 'Vague')
        # scope +2
        opinion1 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[1])
        self.assertEqual(self.solution.get_quality(), 'Good')
        # scope +3
        opinion2 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[2])
        self.assertEqual(self.solution.get_quality(), 'Good')
        # scope +4
        opinion3 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[3])
        self.assertEqual(self.solution.get_quality(), 'Good')
        # scope +5
        opinion4 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[4])
        self.assertEqual(self.solution.get_quality(), 'Approved')
        # scope +6
        opinion5 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[5])
        self.assertEqual(self.solution.get_quality(), 'Approved')
        # scope +7
        opinion6 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[6])
        self.assertEqual(self.solution.get_quality(), 'Approved')
        # scope -1
        opinion0.is_useful = False
        opinion0.full_clean()
        opinion0.save()
        opinion1.is_useful = False
        opinion1.full_clean()
        opinion1.save()
        opinion2.is_useful = False
        opinion2.full_clean()
        opinion2.save()
        opinion3.is_useful = False
        opinion3.full_clean()
        opinion3.save()
        self.assertEqual(self.solution.get_quality(), 'Vague')
        # scope -3
        opinion4.is_useful = False
        opinion4.full_clean()
        opinion4.save()
        self.assertEqual(self.solution.get_quality(), 'Bad')
        # scope -5
        opinion5.is_useful = False
        opinion5.full_clean()
        opinion5.save()
        self.assertEqual(self.solution.get_quality(), 'Heinously')
        # scope -7
        opinion6.is_useful = False
        opinion6.full_clean()
        opinion6.save()
        self.assertEqual(self.solution.get_quality(), 'Heinously')
        # scope -6
        opinion6.delete()
        self.assertEqual(self.solution.get_quality(), 'Heinously')
        # scope -4
        opinion5.delete()
        opinion4.delete()
        self.assertEqual(self.solution.get_quality(), 'Bad')
        # scope -2
        opinion3.delete()
        opinion2.delete()
        self.assertEqual(self.solution.get_quality(), 'Bad')
        # scope 0
        self.solution.opinions.clear()
        self.assertEqual(self.solution.get_quality(), 'Vague')

    def test_get_quality_detail(self):
        # get 5 accounts (exclude author of solution)
        accounts = Account.objects.exclude(pk=self.solution.account.pk).active_accounts().random_accounts(5)
        # Vague quality
        self.solution.opinions.clear()
        self.assertEqual(
            self.solution.get_quality_detail(),
            'Vague quality solution, tells about what solution is have not clear definition of quality.'
        )
        # Good quality
        opinion0 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[0])
        opinion1 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[1])
        opinion2 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[2])
        opinion3 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[3])
        self.assertEqual(
            self.solution.get_quality_detail(),
            'Good quality solution, tells about what solution is have more possitive opinions of users. than negative.'
        )
        # Approved quality
        opinion4 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[4])
        self.assertEqual(
            self.solution.get_quality_detail(),
            'Approved quality solution, tells about what solution is have many possitive opinions from users.'
        )
        # Bad quality
        opinion0.is_useful = False
        opinion0.full_clean()
        opinion0.save()
        opinion1.is_useful = False
        opinion1.full_clean()
        opinion1.save()
        opinion2.is_useful = False
        opinion2.full_clean()
        opinion2.save()
        opinion3.is_useful = False
        opinion3.full_clean()
        opinion3.save()
        self.assertEqual(
            self.solution.get_quality_detail(),
            'Bad quality solution, tells about what solution is have more negative opinions of users, than possitive.'
        )
        # Heinously quality
        opinion4.is_useful = False
        opinion4.full_clean()
        opinion4.save()
        self.assertEqual(
            self.solution.get_quality_detail(),
            'Heinously quality solution, tells about what solution is have many negative opinions from users.'
        )

    def test_critics_of_solution(self):
        # nothing given their opinions
        self.solution.opinions.clear()
        self.assertSequenceEqual(self.solution.critics_of_solution(), [])
        # got distinct users
        accounts = Account.objects.exclude(pk=self.solution.account.pk).active_accounts().random_accounts(5)
        # not critics
        opinion1 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[0])
        opinion2 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[1])
        self.assertSequenceEqual(self.solution.critics_of_solution(), [])
        # presents critics
        opinion3 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[2])
        opinion4 = OpinionFactory(content_object=self.solution, is_useful=False, account=accounts[3])
        opinion5 = OpinionFactory(content_object=self.solution, is_useful=False, account=accounts[4])
        self.assertCountEqual(self.solution.critics_of_solution(), [accounts[3], accounts[4]])
        # some users change their opinions
        opinion1.is_useful = False
        opinion1.full_clean()
        opinion1.save()
        opinion2.is_useful = False
        opinion2.full_clean()
        opinion2.save()
        opinion3.is_useful = False
        opinion3.full_clean()
        opinion3.save()
        opinion4.is_useful = True
        opinion4.full_clean()
        opinion4.save()
        opinion5.is_useful = True
        opinion5.full_clean()
        opinion5.save()
        self.assertSequenceEqual(self.solution.critics_of_solution(), [accounts[0], accounts[1], accounts[2]])

    def test_supporters_of_solution(self):
        # nothing given their opinions
        self.solution.opinions.clear()
        self.assertSequenceEqual(self.solution.supporters_of_solution(), [])
        # got distinct users
        accounts = Account.objects.exclude(pk=self.solution.account.pk).active_accounts().random_accounts(5)
        # not supporters
        opinion1 = OpinionFactory(content_object=self.solution, is_useful=False, account=accounts[0])
        opinion2 = OpinionFactory(content_object=self.solution, is_useful=False, account=accounts[1])
        self.assertSequenceEqual(self.solution.supporters_of_solution(), [])
        # presents supporters
        opinion3 = OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[2])
        opinion4 = OpinionFactory(content_object=self.solution, is_useful=False, account=accounts[3])
        OpinionFactory(content_object=self.solution, is_useful=True, account=accounts[4])
        self.assertCountEqual(self.solution.supporters_of_solution(), [accounts[2], accounts[4]])
        # some users change their opinions
        opinion1.is_useful = True
        opinion1.full_clean()
        opinion1.save()
        opinion2.is_useful = True
        opinion2.full_clean()
        opinion2.save()
        opinion3.is_useful = False
        opinion3.full_clean()
        opinion3.save()
        opinion4.is_useful = True
        opinion4.full_clean()
        opinion4.save()
        self.assertSequenceEqual(self.solution.supporters_of_solution(), [accounts[0], accounts[1], accounts[3], accounts[4]])

    def test_related_solutions(self):
        raise NotImplementedError
