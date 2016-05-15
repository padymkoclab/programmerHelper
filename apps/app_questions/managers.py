
from django.utils import timezone
from django.db import models


class QuestionManager(models.Manager):
    """
    Model manager for model Question
    """

    def questions_with_scopes(self):
        """Auxiliary method for creating field 'scope' for futher proccesing."""
        return self.annotate(scope=models.Sum(
                models.Case(
                    models.When(opinions__is_useful=True, then=1),
                    models.When(opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def non_interesting_questions(self):
        """Filter question with scope 0 or less and without answers."""
        # annotated questions with scopes
        questions_with_scopes = self.questions_with_scopes()
        # questions without answers
        questions_wthput_answers = questions_with_scopes.filter(answers=None)
        # questions without answers and with scope 0 and less
        non_interesting_questions = questions_wthput_answers.exclude(scope__gt=0)
        return non_interesting_questions

    def questions_for_past_24_hours(self):
        """Questions for past 24 hours."""
        now = timezone.now()
        last_24_hours = now - timezone.timedelta(days=1)
        return self.filter(date_added__range=(last_24_hours, now))

    def questions_by_min_count_favorits(self, min_count_favorits):
        """Question with certain minimum count favorites."""
        # annotate questions by favorites
        annotated_questions = self.annotate(favorits=models.Count(
            models.Case(
                models.When(opinions__is_favorite=True, then=1)
                )
            )
        )
        # restrict questions by count favorites
        question_with_certain_favorites = annotated_questions.filter(favorits__gte=min_count_favorits)
        return question_with_certain_favorites

    def questions_by_scopes(self, min_scope=None, max_scope=None):
        """Questions with certain range of scopes."""
        # annotated questions with scopes
        questions_with_scopes = self.questions_with_scopes()
        # restrict
        if min_scope is not None and max_scope is None:
            if isinstance(min_scope, int):
                return questions_with_scopes.filter(scope__gte=min_scope)
            raise ValueError('min_scope is not integer number.')
        elif min_scope is None and max_scope is not None:
            if isinstance(max_scope, int):
                return questions_with_scopes.filter(scope__lte=max_scope)
            raise ValueError('max_scope is not integer number.')
        elif min_scope is not None and max_scope is not None:
            if isinstance(min_scope, int) and isinstance(max_scope, int):
                return questions_with_scopes.filter(scope__gte=min_scope).filter(scope__lte=max_scope)
            raise ValueError('min_scope or max_scope is not integer number.')
        else:
            raise TypeError('Missing 1 required argument: min_scope or max_scope.')


class AnswerManager(models.Manager):
    """
    Model manager for model Answer
    """

    def accepted_answers(self):
        return self.filter(is_accepted=True)

    def answers_with_scopes(self):
        """Auxiliary method for creating field 'scope' for futher proccesing."""
        return self.annotate(scope=models.Sum(
                models.Case(
                    models.When(likes__liked_it=True, then=1),
                    models.When(likes__liked_it=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def answers_by_scopes(self, min_scope=None, max_scope=None):
        """Answers with certain range of scopes."""
        # answers with scopes
        answers_with_scopes = self.answers_with_scopes()
        # restrict
        if min_scope is not None and max_scope is None:
            if isinstance(min_scope, int):
                return answers_with_scopes.filter(scope__gte=min_scope)
            raise ValueError('min_scope is not integer number.')
        elif min_scope is None and max_scope is not None:
            if isinstance(max_scope, int):
                return answers_with_scopes.filter(scope__lte=max_scope)
            raise ValueError('max_scope is not integer number.')
        elif min_scope is not None and max_scope is not None:
            if isinstance(min_scope, int) and isinstance(max_scope, int):
                return answers_with_scopes.filter(scope__gte=min_scope).filter(scope__lte=max_scope)
            raise ValueError('min_scope or max_scope is not integer number.')
        else:
            raise TypeError('Missing 1 required argument: min_scope or max_scope.')

    def answers_for_past_24_hours(self):
        """Answers for past 24 hours."""
        now = timezone.now()
        last_24_hours = now - timezone.timedelta(days=1)
        return self.filter(date_added__range=(last_24_hours, now))

    def quickly_answers(self):
        """Answers published not earlier 24 hours after published their questions."""
        return self.annotate(
            time_after_published_question=models.ExpressionWrapper(
                models.F('date_added') - models.F('question__date_added'),
                output_field=models.DurationField()
            )
        ).filter(time_after_published_question__lte=timezone.timedelta(days=1))

    def revival_answers(self, count_days):
        """Answers published past 7 days after published their questions."""
        return self.annotate(
            time_after_published_question=models.ExpressionWrapper(
                models.F('date_added') - models.F('question__date_added'),
                output_field=models.DurationField()
            )
        ).filter(time_after_published_question__gte=timezone.timedelta(days=7))

    def populistic_answers(self):
        """Answers, what have scope high than accepted answers."""
        accepted_answers = self.accepted_answers()
        for accepted_answer in accepted_answers:
            other_answers_question = accepted_answer.question.answers.exclude(pk=accepted_answer.pk)
            for answer in other_answers_question:
                if answer.get_scope() > accepted_answer.get_scope():
                    print(answer.get_scope(), accepted_answer.get_scope(), answer.question.title)
                    break
