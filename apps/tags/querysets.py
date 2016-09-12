
from django.db import models

from utils.django.models_utils import get_random_objects


class TagQuerySet(models.QuerySet):

    def objects_with_count_tags(self):
        """Added to each object new field with count of tags of the a each object."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))


class PurelyTagQuerySet(models.QuerySet):
    """

    """

    def random_tags(self, count=1, single_as_qs=False):
        """ """

        return get_random_objects(self, count, single_as_qs)

    def tags_with_count_solutions(self):
        """ """

        return self.annotate(count_usage_in_solutions=models.Count('solutions', distinct=True))

    def tags_with_count_articles(self):
        """ """

        return self.annotate(count_usage_in_articles=models.Count('articles', distinct=True))

    def tags_with_count_questions(self):
        """ """

        return self.annotate(count_usage_in_questions=models.Count('questions', distinct=True))

    def tags_with_count_books(self):
        """ """

        return self.annotate(count_usage_in_books=models.Count('books', distinct=True))

    def tags_with_count_snippets(self):
        """ """

        return self.annotate(count_usage_in_snippets=models.Count('snippets', distinct=True))

    def tags_with_total_count_usage(self):
        """ """

        annotated_queryset = self.tags_with_count_solutions().tags_with_count_articles().\
            tags_with_count_questions().tags_with_count_books().tags_with_count_snippets()
        return annotated_queryset.annotate(
            total_count_usage=models.F('count_usage_in_solutions') + models.F('count_usage_in_articles') +
            models.F('count_usage_in_questions') + models.F('count_usage_in_books') +
            models.F('count_usage_in_snippets')
        )

    def less_used_tags(self):
        """Tags used very seldom (from 0 to 3)."""

        raise NotImplementedError
