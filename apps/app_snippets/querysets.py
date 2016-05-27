
from django.db import models


class SnippetQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Snippet
    """

    def snippets_with_scopes(self):
        """Added to each snippet new field 'scope' where storage her scope."""

        return self.annotate(scope=models.Sum(
            models.Case(
                models.When(opinions__is_useful=True, then=1),
                models.When(opinions__is_useful=False, then=-1),
                output_field=models.IntegerField()
            )
        ))

    def snippets_with_count_tags(self):
        """Added to each snippet new field with count of tags of the a each snippet."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))

    def snippets_with_count_opinions(self):
        """Added to each snippet new field with count of opinions of the a each snippet."""

        return self.annotate(count_opinions=models.Count('opinions', distinct=True))

    def snippets_with_count_comments(self):
        """Added to each snippet new field with count of comments of the a each snippet."""

        return self.annotate(count_comments=models.Count('comments', distinct=True))

    def snippets_by_scopes(self, min_scope=None, max_scope=None):
        """Snippets with certain range of scopes."""

        snippets_with_scopes = self.snippets_with_scopes()
        if min_scope is not None and max_scope is None:
            return snippets_with_scopes.filter(scope__gte=min_scope)
        elif min_scope is None and max_scope is not None:
            return snippets_with_scopes.filter(scope__lte=max_scope)
        elif min_scope is not None and max_scope is not None:
            return snippets_with_scopes.filter(scope__gte=min_scope).filter(scope__lte=max_scope)
        else:
            raise TypeError('Missing 1 required argument: "min_scope" or "max_scope".')

    def snippets_with_count_good_opinions(self):
        """ """

        return self.annotate(count_good_opinions=models.Sum(
            models.Case(
                models.When(opinions__is_useful=True, then=1),
                output_field=models.IntegerField()
            )
        ))

    def snippets_with_count_bad_opinions(self):
        """ """

        return self.annotate(count_bad_opinions=models.Sum(
            models.Case(
                models.When(opinions__is_useful=False, then=1),
                output_field=models.IntegerField()
            )
        ))

    def snippets_with_count_tags_opinions_comments_scopes_and_count_good_or_bad_opinions(self):
        return self.snippets_with_count_tags().\
            snippets_with_count_comments().\
            snippets_with_count_opinions().\
            snippets_with_count_good_opinions().\
            snippets_with_count_bad_opinions().\
            snippets_with_scopes()
