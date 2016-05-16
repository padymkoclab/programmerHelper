
from django.db import models


class TestingSuitQuerySet(models.QuerySet):
    """

    """
    pass


class TestingQuestionManager(models.Manager):
    """
    Model manager
    """

    def checkup_what_questions_have_single_right_answer(self):
        for question in self.all():
            if not question.have_one_right_variant():
                print('Problem with question "{0}"'.format(question))
