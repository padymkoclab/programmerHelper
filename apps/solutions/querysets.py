
from django.utils import timezone
from django.db import models

from utils.django.functions_db import ToStr, ToChar


class SolutionCategoryQuerySet(models.QuerySet):
    """
    QuerySet for categories of solutions.
    """

    def categories_with_total_scopes(self):
        """Count up total scope for category of solutions, on based scopes their solutions."""

        raise NotImplementedError
        # try using Value()
        for category in self.prefetch_related('solutions').iterator():
            category_with_scopes_of_solutions = category.solutions.solutions_with_scopes()
            total_scope = category_with_scopes_of_solutions.aggregate(total_scope=models.Sum('scope'))['total_scope']
            category.total_scope = total_scope
        return self

    def categories_with_count_solutions(self):
        """Count solutions for each categories of solutions."""

        return self.annotate(count_solutions=models.Count('solutions', distinct=True))

    def categories_with_latest_activity(self):
        """Determination latest activity in each category of solutions, on based values last modified in their solutions."""

        self = self.annotate(latest_activity=models.Max('solutions__date_modified'))
        self = self.annotate(latest_activity=models.functions.Greatest('latest_activity', 'date_modified'))
        return self

    def categories_with_count_solutions_total_scope_and_latest_activity(self):
        raise NotImplementedError

        self = self.categories_with_latest_activity()
        self = self.categories_with_count_solutions()
        self = self.categories_with_total_scopes()
        return self


class SolutionQuerySet(models.QuerySet):
    """
    QuerySet for solutions.
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

    def solutions_with_displayed_scopes(self):
        """Convert scope of solution to string and return with sign of number:
        if 0 return 0, if 1 return +1, if -1 return -1."""

        self = self.solutions_with_scopes()
        self = self.annotate(scope=ToStr('scope'))
        self = self.annotate(s1=ToChar('scope'))
        # self = self.annotate(displayed_scope=models.Case(
        #     models.When(scope__exact=0, then=models.Value('0')),
        #     models.When(scope__lt=0, then=models.Value('-')),
        #     models.When(scope__gt=0, then=models.Value('+')),
        #     output_field=models.CharField(),
        # ))
        return self

    def solutions_by_scopes(self, min_scope=None, max_scope=None):
        """Solutions with certain range of scopes."""

        # annotated solutions with scopes
        solutions_with_scopes = self.solutions_with_scopes()
        #
        if isinstance(min_scope, int) and isinstance(max_scope, int):
            if min_scope > max_scope:
                raise ValueError('min_scope must not great than max_scope.')
            return solutions_with_scopes.filter(scope__gte=min_scope, scope__lte=max_scope)
        elif isinstance(min_scope, int) and max_scope is None:
            return solutions_with_scopes.filter(scope__gte=min_scope)
        elif min_scope is None and isinstance(max_scope, int):
            return solutions_with_scopes.filter(scope__lte=max_scope)
        elif min_scope is None and max_scope is None:
            raise TypeError('Please give min_scope or max_scope.')
        else:
            raise ValueError('min_scope or max_scope is not integer.')

    def heinously_solutions(self):
        """Solution determined users as heinously by given their opinions."""

        return self.solutions_by_scopes(max_scope=-5)

    def bad_solutions(self):
        """Solution determined users as possibly heinously by given their opinions."""

        return self.solutions_by_scopes(min_scope=-4, max_scope=-2)

    def vague_solutions(self):
        """Solution, what don`t have accurate determined users as heinously or approved."""

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
            models.When(pk__in=self.heinously_solutions(), then=models.Value('Heinously')),
            models.When(pk__in=self.bad_solutions(), then=models.Value('Bad')),
            models.When(pk__in=self.vague_solutions(), then=models.Value('Vague')),
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

    def solutions_by_month(self):
        """Filter solutions added in this month."""

        return self.filter(date_added__month=timezone.now().month)

    def top_solutions_this_month(self):
        """Determined three solutions the best in this month.
        Determination the best solutions based on scope, count views solution and reputation of account."""

        # top for scopes
        self.solutions_with_scopes().order_by('-scope')

        # top for visits

        raise NotImplementedError
