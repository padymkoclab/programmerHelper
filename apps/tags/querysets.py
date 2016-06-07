
from django.db import models

from mylabour.utils import get_random_objects


class TagQuerySet(models.QuerySet):
    """

    """

    def random_tags(self, count=1):
        """ """

        return get_random_objects(self, count)

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