
from django.db import models


class QuestionQuerySet(models.QuerySet):
    """
    Quesryset for questions.
    """

    def questions_with_count_answers(self):
        """ """

        return self.annotate(count_answers=models.Count('answers', distinct=True))

    def unanswered_questions(self):
        """Question without any answers."""

        raise NotImplementedError
        return self

    def questions_with_scope(self):
        """Question with determined scopes."""

        raise NotImplementedError
        return self

    def nasty_questions(self):
        """Question with determined scopes."""

        raise NotImplementedError
        return self

    def bad_questions(self):
        """Question with determined scopes."""

        raise NotImplementedError
        return self

    def vague_questions(self):
        """Question with determined scopes."""

        raise NotImplementedError
        return self

    def good_questions(self):
        """Question with determined scopes."""

        raise NotImplementedError
        return self

    def popular_questions(self):
        """Question with 5 and more answers."""

        raise NotImplementedError
        return self

    def top_questions(self):
        pass

    def top_questions_by_week(self):
        pass

    def queryset_with_all_additional_fields(self):
        """ """

        # self.annotate(count_answers=)

        return self


class AnswerQuerySet(models.QuerySet):
    """

    """

    def queryset_with_all_additional_fields(self):
        """ """

        return self
