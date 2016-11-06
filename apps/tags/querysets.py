
from django.db import models

from utils.django.models_utils import get_random_objects


class TagQuerySet(models.QuerySet):
    """
    Queryset for a manager, using for outside models.
    """

    def objects_with_count_tags(self):
        """Added to each object new field with count of tags of the a each object."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))


class PurelyTagQuerySet(models.QuerySet):
    """
    Queryset for the model Tag
    """

    def random_tags(self, count):
        """ """

        return get_random_objects(self, count)

    def tags_with_total_count_usage(self):
        """ """

        related_fields_names = self.model._get_related_fields_names()

        kwargs = dict()
        for related_field_name in related_fields_names:
            related_field_name

            alias_name = 'count_{}'.format(related_field_name)
            annotation = models.Count(related_field_name, distinct=True)

            kwargs[alias_name] = annotation

        self = self.prefetch_related()
        self = self.annotate(**kwargs)

        CombinedExpression = None
        for alias in kwargs.keys():

            expression = models.F('{}'.format(alias))

            if CombinedExpression is None:
                CombinedExpression = expression
            else:
                CombinedExpression += expression

        condition = dict(total_count_usage=CombinedExpression)

        return self.annotate(**condition)


class UserTagQuerySet(models.QuerySet):
    """

    """

    def users_with_count_used_unique_tags(self):
        """ """

        return self.extra(
            select={
                'count_used_unique_tags': """
                    SELECT COUNT("tag_id") FROM
                    (
                    SELECT "tag_id", "user_id" FROM "snippets" AS Sn
                    LEFT OUTER JOIN "snippets_tags" AS Sntag ON Sntag."snippet_id" = Sn."id"
                    WHERE Sn."user_id" = "users_user"."id"
                    UNION
                    SELECT "tag_id", "user_id" FROM "solutions_solution" AS So
                    LEFT OUTER JOIN "solutions_solution_tags" AS Sotag ON Sotag."solution_id" = So."id"
                    WHERE So."user_id" = "users_user"."id"
                    UNION
                    SELECT "tag_id", "user_id" FROM "questions_question" AS Q
                    LEFT OUTER JOIN "questions_question_tags" AS Qtag ON Qtag."question_id" = Q."id"
                    WHERE Q."user_id" = "users_user"."id"
                    UNION
                    SELECT "tag_id", "user_id" FROM "articles_article" AS A
                    LEFT OUTER JOIN "articles_article_tags" AS Atag ON Atag."article_id" = A."id"
                    WHERE A."user_id" = "users_user"."id"
                    ) AS A
                """
            }
        )

    def users_with_total_count_used_tags(self):
        """ """

        return self.extra(
            select={
                'total_count_used_tags': """
                SELECT COUNT("tag_id") FROM
                    (
                    SELECT "tag_id", "user_id" FROM "snippets" AS Sn
                    LEFT OUTER JOIN "snippets_tags" AS Sntag ON Sntag."snippet_id" = Sn."id"
                    WHERE Sn."user_id" = "users_user"."id"
                    UNION ALL
                    SELECT "tag_id", "user_id" FROM "solutions_solution" AS So
                    LEFT OUTER JOIN "solutions_solution_tags" AS Sotag ON Sotag."solution_id" = So."id"
                    WHERE So."user_id" = "users_user"."id"
                    UNION ALL
                    SELECT "tag_id", "user_id" FROM "questions_question" AS Q
                    LEFT OUTER JOIN "questions_question_tags" AS Qtag ON Qtag."question_id" = Q."id"
                    WHERE Q."user_id" = "users_user"."id"
                    UNION ALL
                    SELECT "tag_id", "user_id" FROM "articles_article" AS A
                    LEFT OUTER JOIN "articles_article_tags" AS Atag ON Atag."article_id" = A."id"
                    WHERE A."user_id" = "users_user"."id"
                    ) AS A
                """,
            }
        )

    def users_with_count_used_unique_tags_and_total_count_used_tags(self):

        self = self.users_with_count_used_unique_tags()
        self = self.users_with_total_count_used_tags()

        return self
