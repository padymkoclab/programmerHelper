
from django.db import models

from apps.opinions.utils import annotate_queryset_for_determinate_rating


class SolutionQuerySet(models.QuerySet):
    """
    QuerySet for solutions.
    """

    def solutions_with_all_additional_fields(self):
        """Solutions with determined: count tags, count links, count opinions, count comments, qualities, ratings."""

        self = self.annotate(count_tags=models.Count('tags', distinct=True))

        self = self.annotate(count_opinions=models.Count('opinions', distinct=True))

        self = self.annotate(count_comments=models.Count('comments', distinct=True))

        self = annotate_queryset_for_determinate_rating(self)

        return self
