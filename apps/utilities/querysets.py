
import logging

from django.db import models

from apps.opinions.utils import annotate_queryset_for_determinate_rating


logger = logging.getLogger('django.development')


class CategoryQuerySet(models.QuerySet):

    def categories_with_count_utilities(self):
        """ """

        self = self.prefetch_related('utilities')
        return self.annotate(count_utilities=models.Count('utilities', distinct=True))

    def categories_with_total_count_opinions(self):
        """ """

        self = self.prefetch_related('utilities__opinions')
        return self.annotate(total_count_opinions=models.Count('utilities__opinions', distinct=True))

    def categories_with_total_count_comments(self):
        """ """

        self = self.prefetch_related('utilities__comments')
        return self.annotate(total_count_comments=models.Count('utilities__comments', distinct=True))

    def categories_with_total_marks(self):
        """ """

        self = self.prefetch_related('utilities__opinions')
        return self.annotate(total_mark=models.Sum(models.Case(
            models.When(utilities__opinions__is_useful=True, then=1),
            models.When(utilities__opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

    def categories_with_all_additional_fields(self):
        """ """

        self = self.categories_with_count_utilities()
        self = self.categories_with_total_count_opinions()
        self = self.categories_with_total_count_comments()

        logger.error('Uncompleted SQL query')

        self = self.categories_with_total_marks()

        # self = self.extra(select={
        #     'total_mark': """
        #     SELECT
        #         SUM(
        #             CASE
        #                 WHEN "opinions"."is_useful" = True THEN 1
        #                 WHEN "opinions"."is_useful" = FALSE THEN -1
        #                 ELSE NULL
        #             END
        #         )
        #     FROM "utilities"
        #     LEFT OUTER JOIN "opinions"
        #         ON ("utilities"."id" = "opinions"."object_id" AND ("opinions"."content_type_id" = 40))
        #     WHERE
        #         "utilities"."id" = "utilities_categories"."id"
        #     GROUP BY "utilities"."id"
        #     """
        # })

        return self


class UtilityQuerySet(models.QuerySet):
    """ """

    def utilities_with_count_opinions(self):
        """ """

        self = self.prefetch_related('opinions')
        return self.annotate(count_opinions=models.Count('opinions', distinct=True))

    def utilities_with_count_comments(self):
        """ """

        self = self.prefetch_related('comments')
        return self.annotate(count_comments=models.Count('comments', distinct=True))

    def utilities_with_rating(self):
        """ """

        self = self.prefetch_related('opinions')
        return self.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

    def utilities_with_all_additional_fields(self):
        """ """

        self = self.utilities_with_count_opinions()
        self = self.utilities_with_count_comments()

        self = annotate_queryset_for_determinate_rating(self)

        return self
