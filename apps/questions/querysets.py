
import logging

from django.db import models

from apps.opinions.utils import annotate_queryset_for_determinate_rating


logger = logging.getLogger(__name__)


class QuestionQuerySet(models.QuerySet):
    """
    Quesryset for questions.
    """

    def questions_with_count_answers(self):
        """ """

        return self.annotate(count_answers=models.Count('answers', distinct=True))

    def top_questions(self):

        raise NotImplementedError

    def top_questions_by_week(self):

        raise NotImplementedError

    def queryset_with_all_additional_fields(self):
        """ """

        self = self.annotate(count_answers=models.Count('answers', distinct=True))
        self = self.annotate(count_flavours=models.Count('flavours', distinct=True))
        self = self.annotate(count_tags=models.Count('tags', distinct=True))
        self = self.annotate(count_opinions=models.Count('opinions', distinct=True))
        self = annotate_queryset_for_determinate_rating(self)

        logger.error('Annotated for field "_has_accepted_answer" does not working')
        self = self.annotate(_has_accepted_answer=models.Case(
            models.When(answers__is_accepted=True, then=None),
            models.When(answers__is_accepted=False, then=None),
            default=None,
            output_field=models.CharField()
        ))

        self = self.annotate(
            date_latest_activity_answers=models.Max('answers__date_modified')
        ).annotate(
            date_latest_activity=models.functions.Coalesce('date_latest_activity_answers', 'date_modified')
        )

        return self


class AnswerQuerySet(models.QuerySet):
    """

    """

    def queryset_with_all_additional_fields(self):
        """ """

        self = self.annotate(count_comments=models.Count('comments', distinct=True))
        self = self.annotate(count_opinions=models.Count('opinions', distinct=True))
        self = annotate_queryset_for_determinate_rating(self)

        return self
