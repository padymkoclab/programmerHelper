
from django.utils import timezone
from django.db import models


class QuestionManager(models.Manager):
    """
    Model manager for model Question
    """

    def non_interesting_questions(self):
        """Filter question with scope 0 or less and without answers"""
        # questions  without answers
        questions = self.filter(answers=None)
        for question in questions:
            if question.get_scope() > 0:
                # exclude redundant question
                questions = questions.exclude(pk=question.pk)
        return questions

    def questions_for_past_24_hours(self):
        """Questions for past 24 hours."""
        now = timezone.now()
        last_24_hours = now - timezone.timedelta(days=1)
        return self.filter(date_added__range=(last_24_hours, now))

    def questions_by_min_count_favorits(self, min_count_favorits):
        """Question with certain minimum count favorites."""
        # annotate questions by favorites
        annotated_questions = self.annotate(favorits=models.Count(models.Case(models.When(opinions__is_favorite=True, then=1))))
        # restrict questions by count favorites
        question_with_certain_favorites = annotated_questions.filter(favorits__gte=min_count_favorits)
        return question_with_certain_favorites

    def questions_by_min_scope(self, min_scope):
        """Question with certain minimun scope."""
        questions = self.filter()
        # restrict questions by mininum scope (inclusive)
        for question in questions:
            if question.get_scope() < min_scope:
                questions = questions.exclude(pk=question.pk)
        return questions


class AnswerManager(models.Manager):
    """
    Model manager for model Answer
    """

    def accepted_answers(self):
        return self.filter(is_accepted=True)

    def answers_by_min_scope(self, min_scope):
        """Answer with certain minimun scope."""
        answers = self.filter()
        # restrict answers by minimum scope (inclusive)
        for answer in answers:
            if answer.get_scope() < min_scope:
                answers = answers.exclude(pk=answer.pk)
        return answers

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
        ).exclude(time_after_published_question__gt=timezone.timedelta(days=1))

    def populistic_answers(self):
        """Answers, what have scope high than accepted answers."""
        accepted_answers = self.accepted_answers()
        for accepted_answer in accepted_answers:
            other_answers_question = accepted_answer.question.answers.exclude(pk=accepted_answer.pk)
            for answer in other_answers_question:
                if answer.get_scope() > accepted_answer.get_scope():
                    print(answer.get_scope(), accepted_answer.get_scope(), answer.question.title)
                    break
