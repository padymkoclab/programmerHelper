
from django.db import models


class QuestionManager(models.Manager):
    """
    Model manager for model Question
    """

    def checkup_what_question_must_be_have_single_accept_answer(self):
        lst = list()
        for question in self.all():
            try:
                question.has_acceptabled_answer()
            except:
                pattern = '{0.title}\n'.format(question)
                lst.append(pattern)
        if lst:
            print('Problems with next questions:')
            print('-'*20)
            print(''.join(lst))
        else:
            print('Alright.')
