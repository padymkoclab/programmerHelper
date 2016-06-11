
from django.db import models


class SolutionCategoryQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model SolutionCategory
    """

    def categories_with_total_scopes(self):
        """Count up total scope for category of solutions, on based scopes their solutions."""

        return self.prefetch_related('solutions').annotate(total_scope=models.Sum('solutions__opinions__is_useful'))
        # return self.annotate(scope=models.Sum(
        #     models.Case(
        #         models.When(opinions__is_useful=True, then=1),
        #         models.When(opinions__is_useful=False, then=-1),
        #         output_field=models.IntegerField()
        #     )
        # ))

    def categories_with_count_solutions(self):
        """Count solutions for each categories of solutions."""

        return self.annotate(count_solutions=models.Count('solutions', distinct=True))

    def categories_with_latest_activity(self):
        """Determination latest activity in each category of solutions, on based values last modified in their solutions."""

        self = self.annotate(latest_activity=models.Max('solutions__date_modified'))
        self = self.annotate(latest_activity=models.functions.Greatest('latest_activity', 'date_modified'))
        return self

    def categories_with_count_solutions_total_scope_and_latest_activity(self):
        self = self.categories_with_latest_activity()
        self = self.categories_with_count_solutions()
        # self = self.categories_with_total_scopes()
        return self


class SolutionQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Solution
    """

    def solutions_with_scopes(self):
        """Added for each solution new field 'scope' where storage her scope."""

        self = self.annotate(scope=models.Sum(
            models.Case(
                models.When(opinions__is_useful=True, then=1),
                models.When(opinions__is_useful=False, then=-1),
                output_field=models.IntegerField()
            )
        ))
        self = self.annotate(scope=models.functions.Coalesce('scope', 0))
        return self

    def solutions_by_scopes(self, min_scope=None, max_scope=None):
        """Solutions with certain range of scopes."""

        # annotated solutions with scopes
        solutions_with_scopes = self.solutions_with_scopes()
        # conditional branches
        if isinstance(min_scope, int) and max_scope is None:
            return solutions_with_scopes.filter(scope__gte=min_scope)
        elif min_scope is None and isinstance(max_scope, int):
            return solutions_with_scopes.filter(scope__lte=max_scope)
        elif min_scope is not None and max_scope is not None:
            if isinstance(min_scope, int) and isinstance(max_scope, int):
                return solutions_with_scopes.filter(scope__gte=min_scope).filter(scope__lte=max_scope)
            raise ValueError('min_scope or max_scope is not integer number.')
        else:
            raise TypeError('Missing 1 required argument: min_scope or max_scope.')

    def wrong_solutions(self):
        """Solution determined users as wrong by given their opinions."""

        return self.solutions_by_scopes(max_scope=-5)

    def bad_solutions(self):
        """Solution determined users as possibly wrong by given their opinions."""

        return self.solutions_by_scopes(min_scope=-4, max_scope=-2)

    def value_solutions(self):
        """Solution, what don`t have accurate determined users as wrong or approved."""

        return self.solutions_by_scopes(min_scope=-1, max_scope=1)

    def good_solutions(self):
        """Solution determined users as possibly approved by given their opinions."""

        return self.solutions_by_scopes(min_scope=2, max_scope=4)

    def approved_solutions(self):
        """Solution determined users as approved by given their opinions."""

        return self.solutions_by_scopes(min_scope=5)

    def solutions_with_qualities(self):
        """Determinate quality of the each solution."""

        solutions_with_scopes = self.solutions_with_scopes()
        return solutions_with_scopes.annotate(quality=models.Case(
            models.When(pk__in=self.wrong_solutions(), then=models.Value('Wrong')),
            models.When(pk__in=self.bad_solutions(), then=models.Value('Bad')),
            models.When(pk__in=self.value_solutions(), then=models.Value('Vague')),
            models.When(pk__in=self.good_solutions(), then=models.Value('Good')),
            models.When(pk__in=self.approved_solutions(), then=models.Value('Approved')),
            output_field=models.CharField(),
        ))

    def solutions_with_count_tags(self):
        """Determinate count tags on each solution and keeping it in new field."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))

    def solutions_with_count_links(self):
        """Determinate count links on each solution and keeping it in new field."""

        return self.annotate(count_links=models.Count('links', distinct=True))

    def solutions_with_count_opinions(self):
        """Determinate count opinions on each solution and keeping it in new field."""

        return self.annotate(count_opinions=models.Count('opinions', distinct=True))

    def solutions_with_count_comments(self):
        """Determinate count comments on each solution and keeping it in new field."""

        return self.annotate(count_comments=models.Count('comments', distinct=True))

    def solutions_with_count_tags_links_opinions_comments_and_quality_scopes(self):
        """Solutions with determined: count tags, count links, count opinions, count comments, qualities, scopes."""

        self = self.solutions_with_count_tags()
        self = self.solutions_with_count_links()
        self = self.solutions_with_count_opinions()
        self = self.solutions_with_count_comments()
        self = self.solutions_with_scopes()
        self = self.solutions_with_qualities()
        return self
