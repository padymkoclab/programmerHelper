
from django.utils import timezone
from django.db import models


class QuestionManager(models.Manager):
    """
    Model manager for model Question
    """

    def get_avg_count_answers(self):
        """ """

        self = self.questions_with_count_answers()
        return self.aggregate(avg=models.Avg('count_answers'))['avg']

    def get_statistics_count_questions_for_the_past_year(self):

        return 1


class AnswerManager(models.Manager):
    """
    Model manager for model Answer
    """

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
