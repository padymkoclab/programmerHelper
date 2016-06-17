
import unittest

from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink

from apps.solutions.factories import solutions_factory, SolutionCategoryFactory, SolutionFactory
from apps.solutions.models import Solution, SolutionCategory


class SolutionCategoryQuerySetTest(TestCase):
    """
    Tests for queryset of categories of solutions.
    """

    @classmethod
    def setUpTestData(self):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        self.category1 = SolutionCategoryFactory()
        self.category2 = SolutionCategoryFactory()
        self.category3 = SolutionCategoryFactory()
        self.category4 = SolutionCategoryFactory()
        self.category5 = SolutionCategoryFactory()

    @unittest.skip('Not implemented')
    def test_categories_with_total_scope(self):
        #
        categories_with_total_scope = SolutionCategory.objects.categories_with_total_scope()
        self.assertEqual(categories_with_total_scope.get(pk=self.category1.pk).total_scope, .0)
        self.assertEqual(categories_with_total_scope.get(pk=self.category2.pk).total_scope, .0)
        self.assertEqual(categories_with_total_scope.get(pk=self.category3.pk).total_scope, .0)
        self.assertEqual(categories_with_total_scope.get(pk=self.category4.pk).total_scope, .0)
        self.assertEqual(categories_with_total_scope.get(pk=self.category5.pk).total_scope, .0)
        # Caterory 1 = -4
        # scope +3
        solution11 = SolutionFactory(category=self.category1)
        OpinionFactory(content_object=solution11, is_useful=True)
        OpinionFactory(content_object=solution11, is_useful=False)
        OpinionFactory(content_object=solution11, is_useful=True)
        OpinionFactory(content_object=solution11, is_useful=True)
        # scope 0
        solution12 = SolutionFactory(category=self.category1)
        OpinionFactory(content_object=solution12, is_useful=True)
        OpinionFactory(content_object=solution12, is_useful=False)
        OpinionFactory(content_object=solution12, is_useful=False)
        OpinionFactory(content_object=solution12, is_useful=True)
        # scope -3
        solution13 = SolutionFactory(category=self.category1)
        OpinionFactory(content_object=solution13, is_useful=True)
        OpinionFactory(content_object=solution13, is_useful=False)
        OpinionFactory(content_object=solution13, is_useful=False)
        OpinionFactory(content_object=solution13, is_useful=False)
        # scope -4
        solution14 = SolutionFactory(category=self.category1)
        OpinionFactory(content_object=solution14, is_useful=False)
        OpinionFactory(content_object=solution14, is_useful=False)
        OpinionFactory(content_object=solution14, is_useful=False)
        OpinionFactory(content_object=solution14, is_useful=False)
        # Category 4 = 4
        # scope 0
        SolutionFactory(category=self.category4)
        # scope 0
        solution42 = SolutionFactory(category=self.category4)
        OpinionFactory(content_object=solution42, is_useful=True)
        OpinionFactory(content_object=solution42, is_useful=False)
        OpinionFactory(content_object=solution42, is_useful=False)
        OpinionFactory(content_object=solution42, is_useful=True)
        # scope 4
        solution43 = SolutionFactory(category=self.category4)
        OpinionFactory(content_object=solution43, is_useful=True)
        OpinionFactory(content_object=solution43, is_useful=True)
        OpinionFactory(content_object=solution43, is_useful=True)
        OpinionFactory(content_object=solution43, is_useful=True)
        # Category 2 = -1
        # scope +2
        solution21 = SolutionFactory(category=self.category2)
        OpinionFactory(content_object=solution21, is_useful=True)
        OpinionFactory(content_object=solution21, is_useful=True)
        # scope -3
        solution23 = SolutionFactory(category=self.category2)
        OpinionFactory(content_object=solution23, is_useful=True)
        OpinionFactory(content_object=solution23, is_useful=False)
        OpinionFactory(content_object=solution23, is_useful=False)
        OpinionFactory(content_object=solution23, is_useful=False)
        # Category 5 = 2
        # scope +2
        solution51 = SolutionFactory(category=self.category5)
        OpinionFactory(content_object=solution51, is_useful=True)
        OpinionFactory(content_object=solution51, is_useful=True)
        #
        categories_with_total_scope = SolutionCategory.objects.categories_with_total_scope()
        self.assertEqual(categories_with_total_scope.get(pk=self.category1.pk).total_scope, -4)
        self.assertEqual(categories_with_total_scope.get(pk=self.category2.pk).total_scope, -1)
        self.assertEqual(categories_with_total_scope.get(pk=self.category3.pk).total_scope, .0)
        self.assertEqual(categories_with_total_scope.get(pk=self.category4.pk).total_scope, 4)
        self.assertEqual(categories_with_total_scope.get(pk=self.category5.pk).total_scope, 2)

    def test_categories_with_count_solutions(self):
        #
        categories_with_count_solutions = SolutionCategory.objects.categories_with_count_solutions()
        self.assertEqual(categories_with_count_solutions.get(pk=self.category1.pk).count_solutions, 0)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category2.pk).count_solutions, 0)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category3.pk).count_solutions, 0)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category4.pk).count_solutions, 0)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category5.pk).count_solutions, 0)
        # generate solutions
        for category, count_solutions in zip(
            [self.category1, self.category2, self.category3, self.category4, self.category5], (2, 11, 0, 1, 7)
        ):
            for i in range(count_solutions):
                SolutionFactory(category=category)
        #
        categories_with_count_solutions = SolutionCategory.objects.categories_with_count_solutions()
        self.assertEqual(categories_with_count_solutions.get(pk=self.category1.pk).count_solutions, 2)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category2.pk).count_solutions, 11)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category3.pk).count_solutions, 0)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category4.pk).count_solutions, 1)
        self.assertEqual(categories_with_count_solutions.get(pk=self.category5.pk).count_solutions, 7)

    def test_categories_with_latest_activity(self):
        #
        categories_with_latest_activity = SolutionCategory.objects.categories_with_latest_activity()
        self.assertEqual(categories_with_latest_activity.get(pk=self.category1.pk).latest_activity, self.category1.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category2.pk).latest_activity, self.category2.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category3.pk).latest_activity, self.category3.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category4.pk).latest_activity, self.category4.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category5.pk).latest_activity, self.category5.date_modified)
        # added solutions
        solution11 = SolutionFactory(category=self.category1)
        solution41 = SolutionFactory(category=self.category4)
        solution51 = SolutionFactory(category=self.category5)
        categories_with_latest_activity = SolutionCategory.objects.categories_with_latest_activity()
        self.assertEqual(categories_with_latest_activity.get(pk=self.category1.pk).latest_activity, solution11.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category2.pk).latest_activity, self.category2.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category3.pk).latest_activity, self.category3.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category4.pk).latest_activity, solution41.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category5.pk).latest_activity, solution51.date_modified)
        # categories were changed
        self.category1.save()
        self.category5.save()
        categories_with_latest_activity = SolutionCategory.objects.categories_with_latest_activity()
        self.assertEqual(categories_with_latest_activity.get(pk=self.category1.pk).latest_activity, self.category1.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category2.pk).latest_activity, self.category2.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category3.pk).latest_activity, self.category3.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category4.pk).latest_activity, solution41.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category5.pk).latest_activity, self.category5.date_modified)
        # added solutions and changed categories
        solution12 = SolutionFactory(category=self.category1)
        solution13 = SolutionFactory(category=self.category1)
        solution14 = SolutionFactory(category=self.category1)
        solution21 = SolutionFactory(category=self.category2)
        solution22 = SolutionFactory(category=self.category2)
        solution23 = SolutionFactory(category=self.category2)
        solution52 = SolutionFactory(category=self.category5)
        categories_with_latest_activity = SolutionCategory.objects.categories_with_latest_activity()
        self.assertEqual(categories_with_latest_activity.get(pk=self.category1.pk).latest_activity, solution14.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category2.pk).latest_activity, solution23.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category3.pk).latest_activity, self.category3.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category4.pk).latest_activity, solution41.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category5.pk).latest_activity, solution52.date_modified)
        # several solutions were changed or deleted
        solution12.save()
        solution13.delete()
        solution14.save()
        solution11.delete()
        solution22.save()
        solution21.delete()
        solution51.delete()
        solution52.delete()
        categories_with_latest_activity = SolutionCategory.objects.categories_with_latest_activity()
        self.assertEqual(categories_with_latest_activity.get(pk=self.category1.pk).latest_activity, solution14.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category2.pk).latest_activity, solution22.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category3.pk).latest_activity, self.category3.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category4.pk).latest_activity, solution41.date_modified)
        self.assertEqual(categories_with_latest_activity.get(pk=self.category5.pk).latest_activity, self.category5.date_modified)

    @unittest.skip('Not implemented')
    def test_categories_with_count_solutions_total_scope_and_latest_activity(self):
        pass


class SolutionQuerySetTest(TestCase):
    """
    Test for queryset of solutions.
    """

    @classmethod
    def setUpTestData(self):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        solutions_factory(10)

    def setUp(self):
        assert Solution.objects.count() == 10, 'This test required strict 10 solutions.'

    def test_solutions_with_scopes(self):
        #
        for solution, opinions in zip(Solution.objects.iterator(), (
            (True, False, False, True, False, False),
            (True, False, False, False, False),
            (True, False, False, True, True, True, True),
            (),
            (False, False, False),
            (True, False, False, False, True, True),
            (True,),
            (False, False, True, True, True, False, False, False, True, True),
            (False,),
            (True, True, True, True),
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        solutions_with_scopes = Solution.objects.solutions_with_scopes()
        self.assertEqual(solutions_with_scopes[0].scope, -2)
        self.assertEqual(solutions_with_scopes[1].scope, -3)
        self.assertEqual(solutions_with_scopes[2].scope, 3)
        self.assertEqual(solutions_with_scopes[3].scope, 0)
        self.assertEqual(solutions_with_scopes[4].scope, -3)
        self.assertEqual(solutions_with_scopes[5].scope, 0)
        self.assertEqual(solutions_with_scopes[6].scope, 1)
        self.assertEqual(solutions_with_scopes[7].scope, 0)
        self.assertEqual(solutions_with_scopes[8].scope, -1)
        self.assertEqual(solutions_with_scopes[9].scope, 4)

    @unittest.skip('Not implemented')
    def test_solutions_with_displayed_opinions(self):
        raise NotImplementedError

    def test_solutions_with_count_comments(self):
        #
        for solution, count_comments in zip(Solution.objects.iterator(), (0, 1, 4, 12, 5, 4, 7, 1, 0, 10)):
            solution.comments.clear()
            for i in range(count_comments):
                CommentFactory(content_object=solution)
        #
        solutions_with_count_comments = Solution.objects.solutions_with_count_comments()
        self.assertEqual(solutions_with_count_comments[0].count_comments, 0)
        self.assertEqual(solutions_with_count_comments[1].count_comments, 1)
        self.assertEqual(solutions_with_count_comments[2].count_comments, 4)
        self.assertEqual(solutions_with_count_comments[3].count_comments, 12)
        self.assertEqual(solutions_with_count_comments[4].count_comments, 5)
        self.assertEqual(solutions_with_count_comments[5].count_comments, 4)
        self.assertEqual(solutions_with_count_comments[6].count_comments, 7)
        self.assertEqual(solutions_with_count_comments[7].count_comments, 1)
        self.assertEqual(solutions_with_count_comments[8].count_comments, 0)
        self.assertEqual(solutions_with_count_comments[9].count_comments, 10)

    def test_solutions_with_count_tags(self):
        for solution, count_tags in zip(Solution.objects.iterator(), (4, 3, 2, 5, 1, 4, 3, 1, 1, 5)):
            tags = [Tag.objects.random_tags(count_tags)] if count_tags == 1 else Tag.objects.random_tags(count_tags)
            solution.tags.set(tags)
        #
        solutions_with_count_tags = Solution.objects.solutions_with_count_tags()
        self.assertEqual(solutions_with_count_tags[0].count_tags, 4)
        self.assertEqual(solutions_with_count_tags[1].count_tags, 3)
        self.assertEqual(solutions_with_count_tags[2].count_tags, 2)
        self.assertEqual(solutions_with_count_tags[3].count_tags, 5)
        self.assertEqual(solutions_with_count_tags[4].count_tags, 1)
        self.assertEqual(solutions_with_count_tags[5].count_tags, 4)
        self.assertEqual(solutions_with_count_tags[6].count_tags, 3)
        self.assertEqual(solutions_with_count_tags[7].count_tags, 1)
        self.assertEqual(solutions_with_count_tags[8].count_tags, 1)
        self.assertEqual(solutions_with_count_tags[9].count_tags, 5)

    def test_solutions_with_count_opinions(self):
        for solution, count_opinions in zip(Solution.objects.iterator(), (1, 6, 2, 0, 11, 7, 0, 1, 0, 5)):
            solution.opinions.clear()
            for i in range(count_opinions):
                OpinionFactory(content_object=solution)
        #
        solutions_with_count_opinions = Solution.objects.solutions_with_count_opinions()
        self.assertEqual(solutions_with_count_opinions[0].count_opinions, 1)
        self.assertEqual(solutions_with_count_opinions[1].count_opinions, 6)
        self.assertEqual(solutions_with_count_opinions[2].count_opinions, 2)
        self.assertEqual(solutions_with_count_opinions[3].count_opinions, 0)
        self.assertEqual(solutions_with_count_opinions[4].count_opinions, 11)
        self.assertEqual(solutions_with_count_opinions[5].count_opinions, 7)
        self.assertEqual(solutions_with_count_opinions[6].count_opinions, 0)
        self.assertEqual(solutions_with_count_opinions[7].count_opinions, 1)
        self.assertEqual(solutions_with_count_opinions[8].count_opinions, 0)
        self.assertEqual(solutions_with_count_opinions[9].count_opinions, 5)

    def test_solutions_with_count_links(self):
        for solution, count_links in zip(Solution.objects.iterator(), (3, 4, 1, 1, 4, 3, 2, 1, 5, 4)):
            links = [WebLink.objects.random_weblinks(count_links)] if count_links == 1 \
                else WebLink.objects.random_weblinks(count_links)
            solution.links.set(links)
        #
        solutions_with_count_links = Solution.objects.solutions_with_count_links()
        self.assertEqual(solutions_with_count_links[0].count_links, 3)
        self.assertEqual(solutions_with_count_links[1].count_links, 4)
        self.assertEqual(solutions_with_count_links[2].count_links, 1)
        self.assertEqual(solutions_with_count_links[3].count_links, 1)
        self.assertEqual(solutions_with_count_links[4].count_links, 4)
        self.assertEqual(solutions_with_count_links[5].count_links, 3)
        self.assertEqual(solutions_with_count_links[6].count_links, 2)
        self.assertEqual(solutions_with_count_links[7].count_links, 1)
        self.assertEqual(solutions_with_count_links[8].count_links, 5)
        self.assertEqual(solutions_with_count_links[9].count_links, 4)

    def test_raises_errors_attempt_getting_solutions_by_scopes(self):
        # if not passed min or max restriction
        self.assertRaisesMessage(
            TypeError,
            'Please give min_scope or max_scope.',
            Solution.objects.solutions_by_scopes
        )
        # if min and max restricts are not integer
        self.assertRaisesMessage(
            ValueError,
            'min_scope or max_scope is not integer.',
            Solution.objects.solutions_by_scopes, 1.1, 2.1
        )
        # if min restrict is more than max restrict
        self.assertRaisesMessage(
            ValueError,
            'min_scope must not great than max_scope.',
            Solution.objects.solutions_by_scopes, 3, 1
        )

    def test_solutions_by_scopes(self):
        #
        for solution, opinions in zip(Solution.objects.iterator(), (
            (True, True, True, True, ),  # 4
            (False, False, False, False, False, False, False, False),  # -8
            (False, False),  # -2
            (True, True, True, True, True, True, True, True, True),  # 9
            (False, False, False, False, False, False),  # -6
            (),  # 0
            (True,),  # 1
            (True, True, True, True, True, True, True, True, True, True, True, True),  # 12
            (True, True, True, True, True, True),  # 6
            (False,),  # -1
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        solutions = Solution.objects.all()
        # restrict by min
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(6), [solutions[3], solutions[7], solutions[8]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(min_scope=-6),
            [
                solutions[0], solutions[2], solutions[3], solutions[4],
                solutions[5], solutions[6], solutions[7], solutions[8], solutions[9]
            ]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(0),
            [solutions[0], solutions[3], solutions[5], solutions[6], solutions[7], solutions[8]]
        )
        # restrict by max
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(max_scope=6),
            [
                solutions[0], solutions[1], solutions[2], solutions[4],
                solutions[5], solutions[6], solutions[8], solutions[9]
            ],
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(max_scope=-6),
            [solutions[1], solutions[4]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(max_scope=0),
            [solutions[1], solutions[2], solutions[4], solutions[5], solutions[9]]
        )
        # restrict by min and max
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(1, 1), [solutions[6]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(0, 9),
            [solutions[0], solutions[3], solutions[5], solutions[6], solutions[8]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(min_scope=-5, max_scope=1),
            [solutions[2], solutions[5], solutions[6], solutions[9]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(0, 1), [solutions[5], solutions[6]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(-8, -6), [solutions[1], solutions[4]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(-8, max_scope=12), solutions
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(-3, 6),
            [solutions[0], solutions[2], solutions[5], solutions[6], solutions[8], solutions[9]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(-20, -8), [solutions[1]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(max_scope=20, min_scope=12), [solutions[7]]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(13, 20), []
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scopes(-1, 1), [solutions[5], solutions[6], solutions[9]]
        )

    @unittest.skip('Not working COUNT and CASE DISTINCT')
    def test_solutions_with_count_tags_links_opinions_comments_and_quality_scopes(self):
        data = (
            {
                'count_tags': 3, 'count_links': 5, 'count_comments': 11,
                'opinions': (True, True, True, True, True, False, True, True),
            },
            {
                'count_tags': 4, 'count_links': 4, 'count_comments': 15,
                'opinions': (False, False, True, True, False, False, False),
            },
            {
                'count_tags': 5, 'count_links': 1, 'count_comments': 6,
                'opinions': (False, ),
            },
            {
                'count_tags': 1, 'count_links': 1, 'count_comments': 5,
                'opinions': (False, False, False, False, True, False, True, False, False, False),
            },
            {
                'count_tags': 2, 'count_links': 2, 'count_comments': 3,
                'opinions': (False, False),
            },
            {
                'count_tags': 4, 'count_links': 3, 'count_comments': 7,
                'opinions': (False, True, True, True, True, True, True, True, True),
            },
            {
                'count_tags': 2, 'count_links': 1, 'count_comments': 0,
                'opinions': (True, False, True, True, False, True, False, True, True, False, True),
            },
            {
                'count_tags': 4, 'count_links': 1, 'count_comments': 1,
                'opinions': (),
            },
            {
                'count_tags': 1, 'count_links': 2, 'count_comments': 2,
                'opinions': (False, False, True, False),
            },
            {
                'count_tags': 5, 'count_links': 5, 'count_comments': 10,
                'opinions': (True, ),
            },
        )

        #
        assert Solution.objects.count() == len(data), 'This test required strict 10 datas of solutions.'

        #
        for solution, data in zip(Solution.objects.iterator(), data):
            solution.comments.clear()
            solution.opinions.clear()
            solution.tags.clear()
            solution.links.clear()
            # generate tags
            count_tags = data['count_tags']
            tags = [Tag.objects.random_tags(count_tags)] if count_tags == 1 \
                else Tag.objects.random_tags(count_tags)
            solution.tags.set(tags)
            # generate links
            count_links = data['count_links']
            links = [WebLink.objects.random_weblinks(count_links)] if count_links == 1 else \
                WebLink.objects.random_weblinks(count_links)
            solution.links.set(links)
            # generate comments
            for i in range(data['count_comments']):
                CommentFactory(content_object=solution)
            # generate opinions
            for opinion in data['opinions']:
                OpinionFactory(content_object=solution, is_useful=opinion)

        #
        solutions = Solution.objects.solutions_with_count_tags_links_opinions_comments_and_quality_scopes()

        # # test count tags
        self.assertEqual(solutions[0].count_tags, 3)
        self.assertEqual(solutions[1].count_tags, 4)
        self.assertEqual(solutions[2].count_tags, 5)
        self.assertEqual(solutions[3].count_tags, 1)
        self.assertEqual(solutions[4].count_tags, 2)
        self.assertEqual(solutions[5].count_tags, 4)
        self.assertEqual(solutions[6].count_tags, 2)
        self.assertEqual(solutions[7].count_tags, 4)
        self.assertEqual(solutions[8].count_tags, 1)
        self.assertEqual(solutions[9].count_tags, 5)

        # test count links
        self.assertEqual(solutions[0].count_links, 5)
        self.assertEqual(solutions[1].count_links, 4)
        self.assertEqual(solutions[2].count_links, 1)
        self.assertEqual(solutions[3].count_links, 1)
        self.assertEqual(solutions[4].count_links, 2)
        self.assertEqual(solutions[5].count_links, 3)
        self.assertEqual(solutions[6].count_links, 1)
        self.assertEqual(solutions[7].count_links, 1)
        self.assertEqual(solutions[8].count_links, 2)
        self.assertEqual(solutions[9].count_links, 5)

        # test count opinions
        self.assertEqual(solutions[0].count_opinions, 8)
        self.assertEqual(solutions[1].count_opinions, 7)
        self.assertEqual(solutions[2].count_opinions, 1)
        self.assertEqual(solutions[3].count_opinions, 10)
        self.assertEqual(solutions[4].count_opinions, 2)
        self.assertEqual(solutions[5].count_opinions, 9)
        self.assertEqual(solutions[6].count_opinions, 11)
        self.assertEqual(solutions[7].count_opinions, 0)
        self.assertEqual(solutions[8].count_opinions, 4)
        self.assertEqual(solutions[9].count_opinions, 1)

        # test count comments
        self.assertEqual(solutions[0].count_comments, 11)
        self.assertEqual(solutions[1].count_comments, 15)
        self.assertEqual(solutions[2].count_comments, 6)
        self.assertEqual(solutions[3].count_comments, 5)
        self.assertEqual(solutions[4].count_comments, 3)
        self.assertEqual(solutions[5].count_comments, 7)
        self.assertEqual(solutions[6].count_comments, 0)
        self.assertEqual(solutions[7].count_comments, 1)
        self.assertEqual(solutions[8].count_comments, 2)
        self.assertEqual(solutions[9].count_comments, 10)

        # test scopes
        self.assertEqual(solutions[0].scope, 6)
        self.assertEqual(solutions[1].scope, -3)
        self.assertEqual(solutions[2].scope, -1)
        self.assertEqual(solutions[3].scope, -6)
        self.assertEqual(solutions[4].scope, -2)
        self.assertEqual(solutions[5].scope, 7)
        self.assertEqual(solutions[6].scope, 3)
        self.assertEqual(solutions[7].scope, 0)
        self.assertEqual(solutions[8].scope, -2)
        self.assertEqual(solutions[9].scope, 1)

        # test quality
        self.assertEqual(solutions[0].quality, 'Approved')
        self.assertEqual(solutions[1].quality, 'Bad')
        self.assertEqual(solutions[2].quality, 'Vague')
        self.assertEqual(solutions[3].quality, 'Heinously')
        self.assertEqual(solutions[4].quality, 'Bad')
        self.assertEqual(solutions[5].quality, 'Approved')
        self.assertEqual(solutions[6].quality, 'Good')
        self.assertEqual(solutions[7].quality, 'Vague')
        self.assertEqual(solutions[8].quality, 'Bad')
        self.assertEqual(solutions[9].quality, 'Vague')

    def test_heinously_solutions(self):
        solutions = Solution.objects.all()
        #
        for solution, opinions in zip(solutions, (
            (),  # 0
            (False, ),  # -1
            (False, False, False, False),  # -4
            (False, False, False, False, False, False, False, False),  # -8
            (False, False),  # -2
            (False, False, False, False, False, False, False, False, False),  # -9
            (False, False, False, False, False, False),  # -6
            (False, False, False, False, False, False, False),  # -7
            (False, False, False, False, False),  # -5
            (False, False, False),  # -3
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        self.assertCountEqual(
            Solution.objects.heinously_solutions(), [solutions[3], solutions[5], solutions[6], solutions[7], solutions[8]]
        )

    def test_bad_solutions(self):
        solutions = Solution.objects.all()
        #
        for solution, opinions in zip(solutions, (
            (),  # 0
            (False, ),  # -1
            (False, False, False, False),  # -4
            (False, False, False, False, False, False, False, False),  # -8
            (False, False),  # -2
            (False, False, False, False, False, False, False, False, False),  # -9
            (False, False, False, False, False, False),  # -6
            (False, False, False, False, False, False, False),  # -7
            (False, False, False, False, False),  # -5
            (False, False, False),  # -3
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        self.assertCountEqual(
            Solution.objects.bad_solutions(), [solutions[2], solutions[4], solutions[9]]
        )

    def test_vague_solutions(self):
        solutions = Solution.objects.all()
        #
        for solution, opinions in zip(solutions, (
            (),  # 0
            (False, ),  # -1
            (True, True, True, True),  # -4
            (True, True, True),  # 3
            (False, False),  # -2
            (True, True),  # 2
            (True, ),  # 1
            (True, True, True, True, True, True),  # 5
            (False, False, False, False, False),  # -5
            (False, False, False),  # -3
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        self.assertCountEqual(
            Solution.objects.vague_solutions(), [solutions[0], solutions[1], solutions[6]]
        )

    def test_good_solutions(self):
        solutions = Solution.objects.all()
        #
        for solution, opinions in zip(solutions, (
            (),  # 0
            (False, ),  # -1
            (True, True, True, True),  # 4
            (True, True, True),  # 3
            (False, False),  # -2
            (True, True),  # 2
            (True, ),  # 1
            (True, True, True, True, True, True),  # 5
            (False, False, False, False, False),  # -5
            (False, False, False),  # -3
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        self.assertCountEqual(
            Solution.objects.good_solutions(), [solutions[2], solutions[3], solutions[5]]
        )

    def test_approved_solutions(self):
        solutions = Solution.objects.all()
        #
        for solution, opinions in zip(solutions, (
            (True, True, True, True, True, True, True, True),  # 7
            (),  # 0
            (False, ),  # -1
            (True, True, True, True),  # -4
            (True, True, True),  # 3
            (True, True, True, True, True, True, True),  # 6
            (True, ),  # 1
            (True, True, True, True, True, True),  # 5
            (False, False, False, False, False),  # -5
            (False, False, False),  # -3
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        self.assertCountEqual(
            Solution.objects.approved_solutions(), [solutions[0], solutions[5], solutions[7]]
        )

    def test_solutions_with_qualities(self):
        # +3 additional solutions
        extra_solution1 = SolutionFactory()
        extra_solution2 = SolutionFactory()
        extra_solution3 = SolutionFactory()
        solutions = Solution.objects.all()
        assert solutions.count() == 13
        #
        for solution, opinions in zip(solutions, (
            (),  # 0
            (False, False, False),  # -3
            (True, True, True, True),  # 4
            (False, False, False, False),  # -4
            (False, False),  # -2
            (True, True),  # 2
            (True, True, True, True, True, True),  # 6
            (False, False, False, False, False, False),  # -6
            (False, ),  # -1
            (True, True, True),  # 3
            (True, ),  # 1
            (False, False, False, False, False),  # -5
            (True, True, True, True, True, True),  # 5
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        solutions_with_qualities = Solution.objects.solutions_with_qualities()
        self.assertEqual(solutions_with_qualities[0].quality, 'Vague')
        self.assertEqual(solutions_with_qualities[1].quality, 'Bad')
        self.assertEqual(solutions_with_qualities[2].quality, 'Good')
        self.assertEqual(solutions_with_qualities[3].quality, 'Bad')
        self.assertEqual(solutions_with_qualities[4].quality, 'Bad')
        self.assertEqual(solutions_with_qualities[5].quality, 'Good')
        self.assertEqual(solutions_with_qualities[6].quality, 'Approved')
        self.assertEqual(solutions_with_qualities[7].quality, 'Heinously')
        self.assertEqual(solutions_with_qualities[8].quality, 'Vague')
        self.assertEqual(solutions_with_qualities[9].quality, 'Good')
        self.assertEqual(solutions_with_qualities[10].quality, 'Vague')
        self.assertEqual(solutions_with_qualities[11].quality, 'Heinously')
        self.assertEqual(solutions_with_qualities[12].quality, 'Approved')
        #
        extra_solution1.delete()
        extra_solution2.delete()
        extra_solution3.delete()

    @unittest.skip('Fuzzy realization of test.')
    def test_solutions_this_month(self):
        solutions = Solution.objects.all()
        assert solutions.count() == 13
        #
        for solution, opinions in zip(solutions, (
            (),  # 0
            (False, False, False),  # -3
            (True, True, True, True),  # 4
            (False, False, False, False),  # -4
            (False, False),  # -2
            (True, True),  # 2
            (True, True, True, True, True, True),  # 6
            (False, False, False, False, False, False),  # -6
            (False, ),  # -1
            (True, True, True),  # 3
            (True, ),  # 1
            (False, False, False, False, False),  # -5
            (True, True, True, True, True, True),  # 5
        )):
            solution.opinions.clear()
            for opinion in opinions:
                OpinionFactory(content_object=solution, is_useful=opinion)
        #
        solutions_with_qualities = Solution.objects.solutions_with_qualities()
        self.assertEqual(solutions_with_qualities[0].quality, 'Vague')
        self.assertEqual(solutions_with_qualities[1].quality, 'Bad')
        self.assertEqual(solutions_with_qualities[2].quality, 'Good')
        self.assertEqual(solutions_with_qualities[3].quality, 'Bad')
        self.assertEqual(solutions_with_qualities[4].quality, 'Bad')
        self.assertEqual(solutions_with_qualities[5].quality, 'Good')
        self.assertEqual(solutions_with_qualities[6].quality, 'Approved')
        self.assertEqual(solutions_with_qualities[7].quality, 'Heinously')
        self.assertEqual(solutions_with_qualities[8].quality, 'Vague')
        self.assertEqual(solutions_with_qualities[9].quality, 'Good')
        self.assertEqual(solutions_with_qualities[10].quality, 'Vague')
        self.assertEqual(solutions_with_qualities[11].quality, 'Heinously')
        self.assertEqual(solutions_with_qualities[12].quality, 'Approved')

    @unittest.skip('Not implemented count visits page')
    def test_top_solutions_this_month(self):
        pass
