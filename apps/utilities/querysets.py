
from django.db import models


class UtilityCategoryQuerySet(models.QuerySet):

    def categories_with_count_utilities(self):
        """ """

        return self.prefetch_related('utilities').annotate(
            count_utilities=models.Count('utilities', distinct=True)
        )

    def categories_with_total_count_opinions(self):
        """ """

        return self

    def categories_with_total_count_comments(self):
        """ """

        return self

    def categories_with_total_mark(self):
        """ """

        return self

    def categories_with_all_additional_fields(self):
        """ """

        self = self.categories_with_count_utilities()
        self = self.categories_with_total_count_opinions()
        self = self.categories_with_total_count_comments()
        self = self.categories_with_total_mark()

        return self


class UtilityQuerySet(models.QuerySet):

    def utilities_with_all_additional_fields(self):
        """ """

        return self
