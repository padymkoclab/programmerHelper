
import random
import logging

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import QuestionFactory, AnswerFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = 'Factory test questions'

    def add_arguments(self, parser):

        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        QuestionModel = QuestionFactory._meta.model
        AnswerModel = AnswerFactory._meta.model

        QuestionModel.objects.filter().delete()

        for i in range(count):
            question = QuestionFactory()

            count_answers = random.randint(0, 10)
            for j in range(count_answers):
                AnswerFactory(question=question)

        logger.critical(
            'Made factory {} questions and {} answers'.format(
                QuestionModel.objects.count(),
                AnswerModel.objects.count(),
            )
        )
