
import random

from mylabour.logging_utils import create_logger_by_filename
from mylabour.basecommands import ExtendedBaseCommand

from ...factories import SuitFactory, TestQuestionFactory, VariantFactory, PassageFactory


logger = create_logger_by_filename(__name__)


class Command(ExtendedBaseCommand):

    help = 'Factory testing suits without testing questions'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        SuitModel = SuitFactory._meta.model
        TestQuestionModel = TestQuestionFactory._meta.model
        VariantModel = VariantFactory._meta.model
        PassageModel = PassageFactory._meta.model

        SuitModel._default_manager.filter().delete()
        PassageModel._default_manager.filter().delete()

        for i in range(count):
            suit = SuitFactory()

            count_questions = random.randint(0, SuitModel.MAX_COUNT_QUESTIONS_FOR_COMPLETED_SUIT)
            for j in range(count_questions):
                question = TestQuestionFactory(suit=suit)

                count_variants = random.randint(0, TestQuestionModel.MAX_COUNT_VARIANTS_FOR_FULL_QUESTION)
                for k in range(count_variants):
                    VariantFactory(question=question)

            exists_count_questions = suit.questions.count()
            if SuitModel.MIN_COUNT_QUESTIONS_FOR_COMPLETED_SUIT <=\
                    exists_count_questions <= SuitModel.MAX_COUNT_QUESTIONS_FOR_COMPLETED_SUIT:
                suit.status = random.choice([SuitModel.UNCOMPLETED, SuitModel.COMPLETED])
                suit.full_clean()
                suit.save()

            if exists_count_questions:
                if 'count_variants' in locals() and count_variants > 0:
                    count_passages = random.randint(0, 15)
                    for e in range(count_passages):
                        PassageFactory(suit=suit)

        logger.debug(
            """
            Succefully factory next objects:
                Suits: {}
                Questions: {}
                Variants: {}
                Passages: {}
            """.format(
                SuitModel._default_manager.count(),
                TestQuestionModel._default_manager.count(),
                VariantModel._default_manager.count(),
                PassageModel._default_manager.count(),
            )
        )
