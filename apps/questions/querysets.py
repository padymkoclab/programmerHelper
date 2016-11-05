
import logging

from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils.django.sql import NullsLastQuerySet

from apps.opinions.models import Opinion

from apps.opinions.utils import annotate_queryset_for_determinate_rating


logger = logging.getLogger('django.delelopment')


class QuestionQuerySet(models.QuerySet):
    """
    Quesryset for questions.
    """

    def objects_with_count_answers(self):
        """ """

        return self.annotate(count_answers=models.Count('answers', distinct=True))

    def objects_with_rating(self):
        """ """

        return annotate_queryset_for_determinate_rating(self)

    def objects_with_count_tags(self):
        """ """

        return self.annotate(count_tags=models.Count('tags', distinct=True))

    def objects_with_count_opinions(self):
        """ """

        return self.annotate(count_opinions=models.Count('opinions', distinct=True))

    def objects_with_date_latest_activity(self):
        """ """

        return self.annotate(
            date_latest_activity_answers=models.Max('answers__updated')
        ).annotate(
            date_latest_activity=models.functions.Coalesce('date_latest_activity_answers', 'updated')
        )

    def top_questions(self):

        raise NotImplementedError

    def top_questions_by_week(self):

        raise NotImplementedError

    def queryset_with_all_additional_fields(self):
        """ """

        self = self.objects_with_count_answers()
        self = self.objects_with_rating()
        self = self.objects_with_count_tags()
        self = self.objects_with_count_opinions()

        logger.error('Annotated for field "_has_accepted_answer" does not working')
        self = self.annotate(_has_accepted_answer=models.Case(
            models.When(answers__is_accepted=True, then=None),
            models.When(answers__is_accepted=False, then=None),
            default=None,
            output_field=models.CharField()
        ))

        self = self.objects_with_date_latest_activity()

        return self


class AnswerQuerySet(models.QuerySet):
    """

    """

    def queryset_with_all_additional_fields(self):
        """ """

        self = self.annotate(count_comments=models.Count('comments', distinct=True))
        self = self.annotate(count_opinions=models.Count('opinions', distinct=True))
        self = self.objects_with_rating()

        return self

    def objects_with_rating(self):
        """ """

        return annotate_queryset_for_determinate_rating(self)


class UserQuestionQuerySet(NullsLastQuerySet):
    """

    """

    def users_with_count_questions(self):

        return self.annotate(count_questions=models.Count('questions', distinct=True))

    def users_with_count_answers_on_questions(self):

        return self.annotate(count_answers_on_questions=models.Count('questions__answers', distinct=True))

    def users_with_count_opinions_on_questions(self):

        return self.annotate(count_opinions_on_questions=models.Count('questions__opinions', distinct=True))

    def users_with_date_latest_question(self):

        return self.annotate(date_latest_question=models.Max('questions__created'))

    def users_with_total_rating_by_questions(self):

        from .models import Question

        return self.extra(
            select={
                'total_rating_questions':
                    """
                    SELECT
                        ROUND(AVG(RATING_FOR_QUESTION), 3)
                    FROM
                        (
                            SELECT
                                {question_table}."user_id",
                                (
                                SELECT
                                    SUM(
                                        CASE
                                            WHEN {opinion_table}."is_useful" = True THEN 1
                                            WHEN {opinion_table}."is_useful" = False THEN -1
                                        END
                                    ) AS RATING_FOR_QUESTION
                                    FROM {opinion_table}
                                    WHERE (
                                        {opinion_table}."object_id" = {question_table}."id" AND
                                            ({opinion_table}."content_type_id" = %s)
                                    )
                                )
                            FROM {question_table}
                        ) AS QUESTION_TABLE
                    WHERE {user_table}."id" = QUESTION_TABLE."user_id"
                    """.format(
                        user_table=self.model._meta.db_table,
                        question_table=Question._meta.db_table,
                        opinion_table=Opinion._meta.db_table,
                    )
            },
            select_params=[ContentType.objects.get_for_model(Question).pk]
        )

    def users_with_count_good_opinions_on_questions(self):

        from .models import Question

        return self.extra(
            select={
                'count_good_opinions_on_questions':
                    """
                    SELECT
                        COUNT(
                            CASE
                                WHEN {opinion_table}."is_useful" = True THEN 1
                            END
                        )
                    FROM {question_table}
                    LEFT OUTER JOIN {opinion_table} ON
                        ({opinion_table}."object_id" = {question_table}."id"
                            AND ({opinion_table}."content_type_id" = %s)
                        )
                    WHERE {user_table}."id" = {question_table}.user_id
                    """.format(
                        user_table=self.model._meta.db_table,
                        question_table=Question._meta.db_table,
                        opinion_table=Opinion._meta.db_table,
                    )
            },
            select_params=[ContentType.objects.get_for_model(Question).pk]
        )

    def users_with_count_bad_opinions_on_questions(self):

        from .models import Question

        return self.extra(
            select={
                'count_bad_opinions_on_questions':
                    """
                    SELECT
                        COUNT(
                            CASE
                                WHEN {opinion_table}."is_useful" = False THEN 1
                            END
                        )
                    FROM {question_table}
                    LEFT OUTER JOIN {opinion_table} ON
                        ({opinion_table}."object_id" = {question_table}."id"
                            AND ({opinion_table}."content_type_id" = %s)
                        )
                    WHERE {user_table}."id" = {question_table}.user_id
                    """.format(
                        user_table=self.model._meta.db_table,
                        question_table=Question._meta.db_table,
                        opinion_table=Opinion._meta.db_table,
                    )
            },
            select_params=[ContentType.objects.get_for_model(Question).pk]
        )

    def users_with_count_questions_and_date_latest_question_and_users_with_rating_by_questions(self):

        self = self.users_with_count_questions()
        self = self.users_with_date_latest_question()
        self = self.users_with_total_rating_by_questions()
        self = self.users_with_count_answers_on_questions()
        self = self.users_with_count_opinions_on_questions()
        self = self.users_with_count_good_opinions_on_questions()
        self = self.users_with_count_bad_opinions_on_questions()

        return self


class UserAnswerQuerySet(models.QuerySet):
    """

    """

    def users_with_count_answers(self):

        return self.annotate(count_answers=models.Count('answers', distinct=True))

    def users_with_count_opinions_on_answers(self):

        return self.annotate(count_opinions=models.Count('answers__opinions', distinct=True))

    def users_with_rating_on_answers(self):

        from .models import Answer

        return self.extra(
            select={
                'total_rating_answers': """
                    SELECT
                        ROUND(AVG(RATING_FOR_ANSWER), 3)
                    FROM
                        (
                            SELECT
                                {answer_table}."user_id",
                                (
                                    SELECT
                                        SUM(
                                            CASE
                                                WHEN {opinion_table}."is_useful" = True THEN 1
                                                WHEN {opinion_table}."is_useful" = False THEN -1
                                            END
                                        )
                                    FROM {opinion_table}
                                    WHERE {opinion_table}."object_id" = {answer_table}."id" AND
                                        ({opinion_table}."content_type_id" = %s)

                                ) AS RATING_FOR_ANSWER
                            FROM {answer_table}
                        ) AS ANSWER_TABLE
                    WHERE ANSWER_TABLE."user_id" = {user_table}."id"
                """.format(
                    opinion_table=Opinion._meta.db_table,
                    answer_table=Answer._meta.db_table,
                    user_table=self.model._meta.db_table,
                )
            },
            select_params=[ContentType.objects.get_for_model(Answer).pk]
        )

    def users_with_count_good_opinions_on_answers(self):

        from .models import Answer

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
                    FROM "{answer_table}"
                    LEFT OUTER JOIN "{opinion_table}"
                        ON "{opinion_table}"."object_id" = "{answer_table}"."id"
                            AND ("{opinion_table}"."content_type_id" = %s)
                    WHERE "{user_table}"."id" = "{answer_table}".user_id
                    """.format(
                        user_table=self.model._meta.db_table,
                        answer_table=Answer._meta.db_table,
                        opinion_table=Opinion._meta.db_table,
                    )
            },
            select_params=[ContentType.objects.get_for_model(Answer).pk]
        )

    def users_with_count_bad_opinions_on_answers(self):

        from .models import Answer

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
                    FROM "{answer_table}"
                    LEFT OUTER JOIN "{opinion_table}"
                        ON "{opinion_table}"."object_id" = "{answer_table}"."id"
                            AND ("{opinion_table}"."content_type_id" = %s)
                    WHERE "{user_table}"."id" = "{answer_table}".user_id
                    """.format(
                        user_table=self.model._meta.db_table,
                        answer_table=Answer._meta.db_table,
                        opinion_table=Opinion._meta.db_table,
                    )
            },
            select_params=[ContentType.objects.get_for_model(Answer).pk]
        )

    def users_with_date_latest_question(self):

        return self.annotate(date_latest_answer=models.Max('answers__created'))

    def users_with_count_comments_on_answers(self):

        return self.annotate(count_comments_answers=models.Count('answers__comments', distinct=True))

    def users_with_count_answers_and_date_latest_answer_and_count_good_bad_total_opinions_on_answers(self):

        self = self.users_with_count_answers()
        self = self.users_with_count_opinions_on_answers()
        self = self.users_with_rating_on_answers()
        self = self.users_with_count_good_opinions_on_answers()
        self = self.users_with_count_bad_opinions_on_answers()
        self = self.users_with_date_latest_question()
        self = self.users_with_count_comments_on_answers()

        return self
