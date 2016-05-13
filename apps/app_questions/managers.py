
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
            if question.get_scope() <= 0:
                # exclude redundant question
                questions = questions.exclude(pk=question.pk)
        return questions


class AnswerManager(models.Manager):
    """
    Model manager for model Answer
    """

    def acceptabled_answers(self):
        return self.filter(is_acceptabled=True)

    def good_answers(self):
        """Acceptabled answers with scope 10 and more."""
        # get acceptabled_answers
        answers = self.acceptabled_answers()
        for answer in answers:
            if answer.get_scope() < 10:
                # exclude redundant answer
                answers = answers.exclude(pk=answer.pk)
        return answers
