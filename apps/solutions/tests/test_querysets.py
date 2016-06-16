
import unittest

from django.utils import timezone
from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.utils import generate_text_certain_length

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

    # def setUp(self):
        # import ipdb; ipdb.set_trace()

    def test_solutions_with_scopes(self):
        solution1, solution2, solution3, solution4 = Solution.objects.all()[:4]
        solution1.opinions.clear()
        solution2.opinions.clear()
        solution3.opinions.clear()
        solution4.opinions.clear()
        #
        OpinionFactory(content_object=solution1, is_useful=True)
        OpinionFactory(content_object=solution1, is_useful=True)
        OpinionFactory(content_object=solution1, is_useful=True)
        OpinionFactory(content_object=solution1, is_useful=False)
        OpinionFactory(content_object=solution1, is_useful=True)
        OpinionFactory(content_object=solution1, is_useful=False)
        OpinionFactory(content_object=solution1, is_useful=True)
        #
        OpinionFactory(content_object=solution2, is_useful=False)
        OpinionFactory(content_object=solution2, is_useful=False)
        OpinionFactory(content_object=solution2, is_useful=True)
        #
        OpinionFactory(content_object=solution3, is_useful=True)
        #
        solutions_with_scopes = Solution.objects.solutions_with_scopes()
        self.assertEqual(solutions_with_scopes.get(pk=solution1.pk).scope, 3)
        self.assertEqual(solutions_with_scopes.get(pk=solution2.pk).scope, -1)
        self.assertEqual(solutions_with_scopes.get(pk=solution3.pk).scope, 1)
        self.assertEqual(solutions_with_scopes.get(pk=solution4.pk).scope, 0)

    @unittest.skip('Not implemented')
    def test_solutions_with_displayed_opinions(self):
        raise NotImplementedError

    def test_solutions_with_count_comments(self):
        assert Solution.objects.count() == 10, 'This test required strict 10 solutions.'
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
        assert Solution.objects.count() == 10, 'This test required strict 10 solutions.'
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
        assert Solution.objects.count() == 10, 'This test required strict 10 solutions.'
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
        assert Solution.objects.count() == 10, 'This test required strict 10 solutions.'
        for solution, count_links in zip(Solution.objects.iterator(), (3, 4, 1, 1, 4, 3, 2, 1, 5, 4)):
            links = [WebLink.objects.random_weblinks(count_links)] if count_links == 1 else WebLink.objects.random_weblinks(count_links)
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

    @unittest.skip('Temporarily skipped')
    def test_solutions_with_scopes_and_count_comments_subsections_tags_links_opinions(self):
        solutions = Solution.objects.all()[:4]
        for solution in solutions:
            solution.subsections.filter().delete()
            solution.comments.clear()
            solution.opinions.clear()
            solution.tags.clear()
            solution.links.clear()
        solution1, solution2, solution3, solution4 = solutions
        #
        solution1.tags.set(Tag.objects.random_tags(5))
        solution1.links.set(WebLink.objects.random_weblinks(5))
        SolutionSubsectionFactory(solution=solution1)
        SolutionSubsectionFactory(solution=solution1)
        SolutionSubsectionFactory(solution=solution1)
        SolutionSubsectionFactory(solution=solution1)
        SolutionSubsectionFactory(solution=solution1)
        CommentFactory(content_object=solution1)
        CommentFactory(content_object=solution1)
        CommentFactory(content_object=solution1)
        CommentFactory(content_object=solution1)
        CommentFactory(content_object=solution1)
        OpinionFactory(content_object=solution1, scope=3)
        OpinionFactory(content_object=solution1, scope=4)
        OpinionFactory(content_object=solution1, scope=1)
        OpinionFactory(content_object=solution1, scope=1)
        OpinionFactory(content_object=solution1, scope=2)
        OpinionFactory(content_object=solution1, scope=3)
        OpinionFactory(content_object=solution1, scope=3)
        OpinionFactory(content_object=solution1, scope=4)
        OpinionFactory(content_object=solution1, scope=5)
        OpinionFactory(content_object=solution1, scope=1)
        OpinionFactory(content_object=solution1, scope=3)
        OpinionFactory(content_object=solution1, scope=2)
        OpinionFactory(content_object=solution1, scope=1)
        #
        solution2.tags.set([Tag.objects.random_tags(1)])
        solution2.links.set([WebLink.objects.random_weblinks(1)])
        SolutionSubsectionFactory(solution=solution2)
        CommentFactory(content_object=solution2)
        OpinionFactory(content_object=solution2, scope=2)
        #
        solution3.tags.set(Tag.objects.random_tags(2))
        solution3.links.set(WebLink.objects.random_weblinks(4))
        SolutionSubsectionFactory(solution=solution3)
        SolutionSubsectionFactory(solution=solution3)
        SolutionSubsectionFactory(solution=solution3)
        CommentFactory(content_object=solution3)
        CommentFactory(content_object=solution3)
        CommentFactory(content_object=solution3)
        CommentFactory(content_object=solution3)
        OpinionFactory(content_object=solution3, scope=1)
        OpinionFactory(content_object=solution3, scope=4)
        OpinionFactory(content_object=solution3, scope=2)
        OpinionFactory(content_object=solution3, scope=2)
        OpinionFactory(content_object=solution3, scope=1)
        OpinionFactory(content_object=solution3, scope=3)
        OpinionFactory(content_object=solution3, scope=4)
        OpinionFactory(content_object=solution3, scope=2)
        #
        solutions = Solution.objects.solutions_with_scopes_and_count_comments_subsections_tags_links_opinions()
        self.assertEqual(solutions.get(pk=solution1.pk).scope, 2.5385)
        self.assertEqual(solutions.get(pk=solution1.pk).count_comments, 5)
        self.assertEqual(solutions.get(pk=solution1.pk).count_subsections, 5)
        self.assertEqual(solutions.get(pk=solution1.pk).count_opinions, 13)
        self.assertEqual(solutions.get(pk=solution1.pk).count_tags, 5)
        self.assertEqual(solutions.get(pk=solution1.pk).count_links, 5)
        self.assertEqual(solutions.get(pk=solution2.pk).scope, 2.0)
        self.assertEqual(solutions.get(pk=solution2.pk).count_comments, 1)
        self.assertEqual(solutions.get(pk=solution2.pk).count_subsections, 1)
        self.assertEqual(solutions.get(pk=solution2.pk).count_opinions, 1)
        self.assertEqual(solutions.get(pk=solution2.pk).count_tags, 1)
        self.assertEqual(solutions.get(pk=solution2.pk).count_links, 1)
        self.assertEqual(solutions.get(pk=solution3.pk).scope, 2.375)
        self.assertEqual(solutions.get(pk=solution3.pk).count_comments, 4)
        self.assertEqual(solutions.get(pk=solution3.pk).count_subsections, 3)
        self.assertEqual(solutions.get(pk=solution3.pk).count_opinions, 8)
        self.assertEqual(solutions.get(pk=solution3.pk).count_tags, 2)
        self.assertEqual(solutions.get(pk=solution3.pk).count_links, 4)
        self.assertEqual(solutions.get(pk=solution4.pk).scope, 0)
        self.assertEqual(solutions.get(pk=solution4.pk).count_comments, 0)
        self.assertEqual(solutions.get(pk=solution4.pk).count_subsections, 0)
        self.assertEqual(solutions.get(pk=solution4.pk).count_opinions, 0)
        self.assertEqual(solutions.get(pk=solution4.pk).count_tags, 0)
        self.assertEqual(solutions.get(pk=solution4.pk).count_links, 0)

    @unittest.skip('Temporarily skipped')
    def test_published_solutions(self):
        # all published solutions
        Solution.objects.update(status=Solution.STATUS_ARTICLE.published)
        self.assertEqual(Solution.objects.published_solutions().count(), 10)
        # not published solutions
        Solution.objects.update(status=Solution.STATUS_ARTICLE.draft)
        self.assertEqual(Solution.objects.published_solutions().count(), 0)
        # two solutions are published, other - not
        first_solution = Solution.objects.first()
        first_solution.status = Solution.STATUS_ARTICLE.published
        first_solution.full_clean()
        first_solution.save()
        last_solution = Solution.objects.last()
        last_solution.status = Solution.STATUS_ARTICLE.published
        last_solution.full_clean()
        last_solution.save()
        self.assertEqual(Solution.objects.published_solutions().count(), 2)
        # reset
        Solution.objects.update(status=Solution.STATUS_ARTICLE.draft)
        # each second solution is published
        pks = Solution.objects.values_list('pk', flat=True)[::2]
        Solution.objects.filter(pk__in=pks).update(status=Solution.STATUS_ARTICLE.published)
        self.assertEqual(Solution.objects.published_solutions().count(), 5)

    @unittest.skip('Temporarily skipped')
    def test_draft_solutions(self):
        # all draft solutions
        Solution.objects.update(status=Solution.STATUS_ARTICLE.draft)
        self.assertEqual(Solution.objects.draft_solutions().count(), 10)
        Solution.objects.update(status=Solution.STATUS_ARTICLE.published)
        # two solutions are draft, other - not
        first_solution = Solution.objects.first()
        first_solution.status = Solution.STATUS_ARTICLE.draft
        first_solution.full_clean()
        first_solution.save()
        last_solution = Solution.objects.last()
        last_solution.status = Solution.STATUS_ARTICLE.draft
        last_solution.full_clean()
        last_solution.save()
        self.assertEqual(Solution.objects.draft_solutions().count(), 2)
        # not draft solutions
        Solution.objects.update(status=Solution.STATUS_ARTICLE.published)
        self.assertEqual(Solution.objects.draft_solutions().count(), 0)
        # each second solution is draft
        pks = Solution.objects.values_list('pk', flat=True)[::2]
        Solution.objects.filter(pk__in=pks).update(status=Solution.STATUS_ARTICLE.draft)
        self.assertEqual(Solution.objects.draft_solutions().count(), 5)

    @unittest.skip('Temporarily skipped')
    def test_weekly_solutions(self):
        now = timezone.now()
        for solution in Solution.objects.iterator():
            solution.date_added = now - timezone.timedelta(days=8)
            solution.full_clean()
            solution.save()
        self.assertEqual(Solution.objects.weekly_solutions().count(), 0)
        dates = [
            # satisfy dates
            now,
            now - timezone.timedelta(days=1),
            now - timezone.timedelta(days=2),
            now - timezone.timedelta(days=3),
            now - timezone.timedelta(days=4),
            now - timezone.timedelta(days=5),
            now - timezone.timedelta(days=6),
            now - timezone.timedelta(days=6, hours=23, minutes=59, seconds=59),
            # not satisfy dates
            now - timezone.timedelta(days=7),
            now - timezone.timedelta(days=8),
            now - timezone.timedelta(days=9),
        ]
        for date, solution in zip(dates, Solution.objects.all()):
            solution.date_added = date
            solution.full_clean()
            solution.save()
        self.assertEqual(Solution.objects.weekly_solutions().count(), 8)

    @unittest.skip('Temporarily skipped')
    def test_solutions_from_external_resourse(self):
        # all solutions is own of site
        Solution.objects.update(source=None)
        self.assertEqual(Solution.objects.solutions_from_external_resourse().count(), 0)
        # two solutions are external, other - not
        first_solution = Solution.objects.first()
        first_solution.source = 'http://zabuto.js/simple_and_stupid_development.html'
        first_solution.full_clean()
        first_solution.save()
        last_solution = Solution.objects.last()
        last_solution.source = 'http://tornado.com/best_web_server_for_python/'
        last_solution.full_clean()
        last_solution.save()
        self.assertEqual(Solution.objects.solutions_from_external_resourse().count(), 2)
        # all solutions is external
        Solution.objects.update(source='http://djangoproject.com/models')
        self.assertEqual(Solution.objects.solutions_from_external_resourse().count(), 10)
        # reset
        Solution.objects.update(source=None)
        # each second solution is external
        pks = Solution.objects.values_list('pk', flat=True)[::2]
        Solution.objects.filter(pk__in=pks).update(source='http://python.org/how_to_made')
        self.assertEqual(Solution.objects.solutions_from_external_resourse().count(), 5)

    @unittest.skip('Temporarily skipped')
    def test_own_solutions(self):
        # all solutions is own of site
        Solution.objects.update(source=None)
        self.assertEqual(Solution.objects.own_solutions().count(), 10)
        # two solutions are external, other - not
        first_solution = Solution.objects.first()
        first_solution.source = 'http://jquery.js/simple_and_stupid_development.html'
        first_solution.full_clean()
        first_solution.save()
        last_solution = Solution.objects.last()
        last_solution.source = 'http://tornado.com/best_web_server_for_python/'
        last_solution.full_clean()
        last_solution.save()
        self.assertEqual(Solution.objects.own_solutions().count(), 8)
        # all solutions is external
        Solution.objects.update(source='http://djangoproject.com/models')
        self.assertEqual(Solution.objects.own_solutions().count(), 0)
        # reset
        Solution.objects.update(source=None)
        # each second solution is external
        pks = Solution.objects.values_list('pk', flat=True)[::2]
        Solution.objects.filter(pk__in=pks).update(source='http://python.org/how_to_made')
        self.assertEqual(Solution.objects.own_solutions().count(), 5)

    @unittest.skip('Temporarily skipped')
    def test_hot_solutions(self):
        """Test what each solution with count comments 7 and more enters in categories "Hot" solutions."""

        for solution in Solution.objects.iterator():
            solution.comments.clear()
        self.assertEqual(Solution.objects.hot_solutions().count(), 0)
        for count_comments, solution in enumerate(Solution.objects.all()):
            for i in range(count_comments):
                CommentFactory(content_object=solution)
        self.assertCountEqual(Solution.objects.hot_solutions(), Solution.objects.all()[::-1][:3])

    @unittest.skip('Temporarily skipped')
    def test_popular_solutions(self):
        """Test what each solution with scope 5 and more consider as popular."""

        for solution in Solution.objects.iterator():
            solution.opinions.clear()
        self.assertEqual(Solution.objects.popular_solutions().count(), 0)
        solution1, solution2, solution3, solution4, solution5 = Solution.objects.all()[:5]
        # 4
        OpinionFactory(content_object=solution1, scope=4)
        # 54 / 11
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=5)
        OpinionFactory(content_object=solution2, scope=4)
        self.assertEqual(solution2.get_scope(), 4.9091)
        # 5
        OpinionFactory(content_object=solution3, scope=5)
        # 45 / 11
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=2)
        OpinionFactory(content_object=solution4, scope=2)
        OpinionFactory(content_object=solution4, scope=1)
        self.assertEqual(solution4.get_scope(), 4.0909)
        #
        self.assertCountEqual(Solution.objects.popular_solutions(), [solution1, solution2, solution3, solution4])

    @unittest.skip('Temporarily skipped')
    def test_validate_input_solutions_by_scope(self):
        # if not nothing limitation
        self.assertRaisesMessage(
            AttributeError,
            'Please point at least either min_scope or max_scope.',
            Solution.objects.solutions_by_scope
        )
        # if max_scope is less than min_scope
        self.assertRaisesMessage(
            ValueError,
            'Don`t right values: min_scope is more than max_scope.',
            Solution.objects.solutions_by_scope,
            2,
            1
        )

    @unittest.skip('Temporarily skipped')
    def test_solutions_by_scope(self):

        for solution in Solution.objects.iterator():
            solution.opinions.clear()
        solution1, solution2, solution3, solution4, solution5, solution6, solution7 = Solution.objects.all()[:7]
        Solution.objects.exclude(pk__in=Solution.objects.values('pk')[:7]).delete()
        # 3
        OpinionFactory(content_object=solution1, scope=2)
        OpinionFactory(content_object=solution1, scope=3)
        OpinionFactory(content_object=solution1, scope=4)
        # 4.3333
        OpinionFactory(content_object=solution2, scope=4)
        OpinionFactory(content_object=solution2, scope=4)
        OpinionFactory(content_object=solution2, scope=5)
        # 5
        OpinionFactory(content_object=solution3, scope=5)
        OpinionFactory(content_object=solution3, scope=5)
        OpinionFactory(content_object=solution3, scope=5)
        # 3.6666
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=5)
        OpinionFactory(content_object=solution4, scope=1)
        # 2.6667
        OpinionFactory(content_object=solution5, scope=1)
        OpinionFactory(content_object=solution5, scope=4)
        OpinionFactory(content_object=solution5, scope=3)
        # 1.6667
        OpinionFactory(content_object=solution6, scope=1)
        OpinionFactory(content_object=solution6, scope=1)
        OpinionFactory(content_object=solution6, scope=3)
        # 1
        OpinionFactory(content_object=solution7, scope=1)
        OpinionFactory(content_object=solution7, scope=1)
        OpinionFactory(content_object=solution7, scope=1)
        # find by min scope
        self.assertCountEqual(
            Solution.objects.solutions_by_scope(min_scope=1),
            [solution1, solution2, solution3, solution4, solution5, solution6, solution7]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scope(min_scope=2),
            [solution1, solution2, solution3, solution4, solution5],
        )
        self.assertCountEqual(Solution.objects.solutions_by_scope(min_scope=2.7), [solution1, solution2, solution3, solution4])
        self.assertCountEqual(Solution.objects.solutions_by_scope(min_scope=3.1), [solution2, solution3, solution4])
        self.assertCountEqual(Solution.objects.solutions_by_scope(min_scope=3.9), [solution2, solution3])
        # find by max scope
        self.assertCountEqual(Solution.objects.solutions_by_scope(max_scope=1), [solution7])
        self.assertCountEqual(Solution.objects.solutions_by_scope(max_scope=2), [solution6, solution7])
        self.assertCountEqual(Solution.objects.solutions_by_scope(max_scope=3.1), [solution1, solution5, solution6, solution7])
        self.assertCountEqual(
            Solution.objects.solutions_by_scope(max_scope=3.9),
            [solution1, solution4, solution5, solution6, solution7]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scope(max_scope=4.7),
            [solution1, solution2, solution4, solution5, solution6, solution7]
        )
        # find by min and max limitations of scope
        self.assertCountEqual(
            Solution.objects.solutions_by_scope(1, 3),
            [solution1, solution5, solution6, solution7]
        )
        self.assertCountEqual(
            Solution.objects.solutions_by_scope(2, 5),
            [solution1, solution2, solution3, solution4, solution5],
        )
        self.assertCountEqual(Solution.objects.solutions_by_scope(2.7, 3.5), [solution1])
        self.assertCountEqual(Solution.objects.solutions_by_scope(3.1, 4.8), [solution2, solution4])
        self.assertCountEqual(Solution.objects.solutions_by_scope(3.9, 5), [solution2, solution3])
        self.assertCountEqual(Solution.objects.solutions_by_scope(1.8, 1.9), [])

    @unittest.skip('Temporarily skipped')
    def test_big_solutions(self):
        for solution in Solution.objects.iterator():
            solution.subsections.filter().delete()
            solution.header = 'This is simple solution about Python and JS.'
            solution.conclusion = 'I decided what Python and JS is neccesary for each web-developer.'
            solution.full_clean()
            solution.save()
        solution1, solution2, solution3, solution4, solution5 = Solution.objects.all()[:5]
        self.assertEqual(Solution.objects.big_solutions().count(), 0)
        #
        solution1.header = generate_text_certain_length(10000)
        solution1.full_clean()
        solution1.save()
        self.assertCountEqual(Solution.objects.big_solutions(), [solution1])
        #
        solution2.conclusion = generate_text_certain_length(10000)
        solution2.full_clean()
        solution2.save()
        self.assertCountEqual(Solution.objects.big_solutions(), [solution1, solution2])
        #
        SolutionSubsectionFactory(solution=solution3, content=generate_text_certain_length(10000))
        self.assertCountEqual(Solution.objects.big_solutions(), [solution1, solution2, solution3])
        #
        SolutionSubsectionFactory(solution=solution4, content=generate_text_certain_length(3000))
        SolutionSubsectionFactory(solution=solution4, content=generate_text_certain_length(3000))
        SolutionSubsectionFactory(solution=solution4, content=generate_text_certain_length(4000))
        self.assertCountEqual(Solution.objects.big_solutions(), [solution1, solution2, solution3, solution4])
        #
        SolutionSubsectionFactory(solution=solution5, content=generate_text_certain_length(9000))
        self.assertCountEqual(Solution.objects.big_solutions(), [solution1, solution2, solution3, solution4])
