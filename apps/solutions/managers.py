
import random

from django.db import models


class SolutionQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Solution
    """

    def solutions_with_scopes(self):
        """Added for each solution new field 'scope' where storage her scope."""

        return self.annotate(scope=models.Sum(
            models.Case(
                models.When(opinions__is_useful=True, then=1),
                models.When(opinions__is_useful=False, then=-1),
                output_field=models.IntegerField()
            )
        ))

    def solutions_by_scopes(self, min_scope=None, max_scope=None):
        """Solutions with certain range of scopes."""
        # annotated solutions with scopes
        solutions_with_scopes = self.solutions_with_scopes()
        # conditional branches
        if min_scope is not None and max_scope is None:
            return solutions_with_scopes.filter(scope__gte=min_scope)
        elif min_scope is None and max_scope is not None:
            return solutions_with_scopes.filter(scope__lte=max_scope)
        elif min_scope is not None and max_scope is not None:
            if isinstance(min_scope, int) and isinstance(max_scope, int):
                return solutions_with_scopes.filter(scope__gte=min_scope).filter(scope__lte=max_scope)
            raise ValueError('min_scope or max_scope is not integer number.')
        else:
            raise TypeError('Missing 1 required argument: min_scope or max_scope.')


class SolutionCategoryManager(models.Manager):
    """
    Model manager
    """

    def get_random_category(self):
        random_pk = random.choice(self.values_list('pk', flat=True))
        return self.get(pk=random_pk)
