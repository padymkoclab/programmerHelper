
from django.db import models
from django.contrib.contenttypes.models import ContentType

from apps.opinions.utils import annotate_queryset_for_determinate_rating
from apps.opinions.models import Opinion


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

    def objects_with_rating(self):
        """ """

        return annotate_queryset_for_determinate_rating(self)


class UserSolutionQuerySet(models.QuerySet):
    """

    """

    def users_with_rating_of_solutions(self):
        """ """

        return annotate_queryset_for_determinate_rating(self)

    def users_with_count_solutions(self):

        return self.annotate(count_solutions=models.Count('solutions', distinct=True))

    def users_with_count_opinions_of_solutions(self):

        return self.annotate(count_opinions_solutions=models.Count('solutions__opinions', distinct=True))

    def users_with_count_bad_opinions_of_solutions(self):

        from .models import Solution

        return self.extra(
            select={
                'count_bad_opinions':
                    """
                    SELECT
                        COUNT(
                            CASE
                                WHEN {opinion_table}."is_useful" = False THEN 1
                            END
                        )
                    FROM "{solutions_table}"
                    LEFT OUTER JOIN "{opinion_table}"
                        ON "{opinion_table}"."object_id" = "{solutions_table}"."id"
                            AND ("{opinion_table}"."content_type_id" = %s)
                    WHERE "{user_table}"."id" = "{solutions_table}".user_id
                    """.format(
                        user_table=self.model._meta.db_table,
                        solutions_table=Solution._meta.db_table,
                        opinion_table=Opinion._meta.db_table,
                    )
            },
            select_params=[ContentType.objects.get_for_model(Solution).pk]
        )

    def users_with_count_good_opinions_of_solutions(self):

        from .models import Solution

        return self.extra(
            select={
                'count_good_opinions':
                    """
                    SELECT
                        COUNT(
                            CASE
                                WHEN {opinion_table}."is_useful" = True THEN 1
                            END
                        )
                    FROM "{solutions_table}"
                    LEFT OUTER JOIN "{opinion_table}"
                        ON "{opinion_table}"."object_id" = "{solutions_table}"."id"
                            AND ("{opinion_table}"."content_type_id" = %s)
                    WHERE "{user_table}"."id" = "{solutions_table}".user_id
                    """.format(
                        user_table=self.model._meta.db_table,
                        solutions_table=Solution._meta.db_table,
                        opinion_table=Opinion._meta.db_table,
                    )
            },
            select_params=[ContentType.objects.get_for_model(Solution).pk]
        )

    def users_with_count_comments_of_solutions(self):

        return self.annotate(count_comments_solutions=models.Count('solutions__comments', distinct=True))

    def users_with_date_latest_solution(self):

        return self.annotate(date_latest_solution=models.Max('solutions__created'))

    def users_with_count_comments_solutions_bad_good_and_total_opinions_and_rating_and_date_latest_solutions(self):

        # self = self.users_with_rating_of_solutions()
        self = self.users_with_count_solutions()
        self = self.users_with_count_opinions_of_solutions()
        self = self.users_with_count_bad_opinions_of_solutions()
        self = self.users_with_count_good_opinions_of_solutions()
        self = self.users_with_count_comments_of_solutions()
        self = self.users_with_date_latest_solution()

        return self
