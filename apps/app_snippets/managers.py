
from django.db import models


class SnippetQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Snippet
    """

    def snippets_with_scopes(self, queryset=None):
        """Added for each snippet new field 'scope' where storage her scope."""

        return self.annotate(scope=models.Sum(
                models.Case(
                    models.When(opinions__is_useful=True, then=1),
                    models.When(opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def snippets_by_scopes(self, min_scope=None, max_scope=None):
        """Snippets with certain range of scopes."""
        # annotated snippets with scopes
        snippets_with_scopes = self.snippets_with_scopes()
        # conditional branches
        if min_scope is not None and max_scope is None:
            return snippets_with_scopes.filter(scope__gte=min_scope)
        elif min_scope is None and max_scope is not None:
            return snippets_with_scopes.filter(scope__lte=max_scope)
        elif min_scope is not None and max_scope is not None:
            if isinstance(min_scope, int) and isinstance(max_scope, int):
                return snippets_with_scopes.filter(scope__gte=min_scope).filter(scope__lte=max_scope)
            raise ValueError('min_scope or max_scope is not integer number.')
        else:
            raise TypeError('Missing 1 required argument: min_scope or max_scope.')


class SnippetManager(models.Manager):
    """
    Model manager
    """

    pass
