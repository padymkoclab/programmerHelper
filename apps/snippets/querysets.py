
from django.db import models
from django.contrib.contenttypes.models import ContentType

from utils.django.sql import NullsLastQuerySet

from apps.opinions.utils import annotate_queryset_for_determinate_rating
from apps.opinions.models import Opinion


class SnippetQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Snippet
    """

    def snippets_by_marks(self, min_mark=None, max_mark=None):
        """Snippets with certain range of marks."""

        objects_with_marks = self.objects_with_marks()
        if min_mark is not None and max_mark is None:
            return objects_with_marks.filter(mark__gte=min_mark)
        elif min_mark is None and max_mark is not None:
            return objects_with_marks.filter(mark__lte=max_mark)
        elif min_mark is not None and max_mark is not None:
            return objects_with_marks.filter(mark__gte=min_mark).filter(mark__lte=max_mark)
        else:
            raise TypeError('Missing 1 required argument: "min_mark" or "max_mark".')

    def snippets_with_all_additional_fields(self):
        """Determinating for each snippet count_tags, opinions, favours, comments,
        getting mark, count good/bad opinions, and count likes/dislikes favours."""

        self = self.annotate(count_tags=models.Count('tags', distinct=True))

        self = self.annotate(count_opinions=models.Count('opinions', distinct=True))

        self = self.annotate(count_comments=models.Count('comments', distinct=True))

        self = annotate_queryset_for_determinate_rating(self)

        return self

    def objects_with_rating(self):
        """ """

        return annotate_queryset_for_determinate_rating(self)


class UserSnippetQuerySet(NullsLastQuerySet):
    """

    """

    def users_with_count_snippets(self):

        return self.annotate(count_snippets=models.Count('snippets', distinct=True))

    def users_with_count_opinions(self):

        return self.annotate(count_opinions_snippets=models.Count('snippets__opinions', distinct=True))

    def users_with_count_comments(self):

        return self.annotate(count_comments_snippets=models.Count('snippets__comments', distinct=True))

    def users_with_total_rating_on_snippets(self):

        from .models import Snippet

        return self.extra(
            select={
                'total_rating_snippets': """
                SELECT
                    ROUND(AVG(RATING_FOR_SNIPPET), 3)
                FROM
                    (
                        SELECT
                            {snippet_table}."user_id",
                            (
                                SELECT
                                    SUM(
                                        CASE
                                            WHEN {opinion_table}."is_useful" = True THEN 1
                                            WHEN {opinion_table}."is_useful" = False THEN -1
                                        END
                                    ) AS RATING_FOR_SNIPPET
                                    FROM {opinion_table}
                                    WHERE {opinion_table}."object_id" = {snippet_table}."id" AND
                                        ({opinion_table}."content_type_id" = %s)
                            )
                        FROM {snippet_table}
                    ) AS TABLE_SNIPPET
                WHERE TABLE_SNIPPET."user_id" = {user_table}."id"
                """.format(
                    opinion_table=Opinion._meta.db_table,
                    snippet_table=Snippet._meta.db_table,
                    user_table=self.model._meta.db_table,
                )
            },
            select_params=[ContentType.objects.get_for_model(Snippet).pk]
        )

    def users_with_count_good_opinions_on_snippets(self):

        from .models import Snippet

        return self.extra(
            select={
                'count_good_opinions_snippets': """
                SELECT
                    COUNT(*)
                FROM {snippet_table}
                LEFT OUTER JOIN {opinion_table} ON {opinion_table}."object_id" = {snippet_table}."id"
                    AND ({opinion_table}."content_type_id" = %s)
                WHERE {user_table}."id" = {snippet_table}."user_id" AND ({opinion_table}."is_useful" = True)
                """.format(
                    snippet_table=Snippet._meta.db_table,
                    opinion_table=Opinion._meta.db_table,
                    user_table=self.model._meta.db_table,
                )
            },
            select_params=[ContentType.objects.get_for_model(Snippet).pk]
        )

    def users_with_count_bad_opinions_on_snippets(self):

        from .models import Snippet

        return self.extra(
            select={
                'count_bad_opinions_snippets': """
                SELECT
                    COUNT(*)
                FROM {snippet_table}
                LEFT OUTER JOIN {opinion_table} ON {opinion_table}."object_id" = {snippet_table}."id"
                    AND ({opinion_table}."content_type_id" = %s)
                WHERE {user_table}."id" = {snippet_table}."user_id" AND ({opinion_table}."is_useful" = False)
                """.format(
                    snippet_table=Snippet._meta.db_table,
                    opinion_table=Opinion._meta.db_table,
                    user_table=self.model._meta.db_table,
                )
            },
            select_params=[ContentType.objects.get_for_model(Snippet).pk]
        )

    def users_with_date_latest_snippet(self):

        return self.annotate(date_latest_snippet=models.Max('snippets__created'))

    def users_with_count_comments_bad_good_and_total_opinions_and_rating_and_date_latest_snippets(self):

        self = self.users_with_count_snippets()
        self = self.users_with_count_opinions()
        self = self.users_with_count_comments()
        self = self.users_with_count_good_opinions_on_snippets()
        self = self.users_with_count_bad_opinions_on_snippets()
        self = self.users_with_total_rating_on_snippets()
        self = self.users_with_date_latest_snippet()

        return self
