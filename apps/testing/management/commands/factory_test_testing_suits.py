
import logging
import random

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import SuitFactory, QuestionFactory, VariantFactory, PassageFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    help = 'Factory testing suits without testing questions'

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        SuitModel = SuitFactory._meta.model
        QuestionModel = QuestionFactory._meta.model
        VariantModel = VariantFactory._meta.model
        PassageModel = PassageFactory._meta.model

        SuitModel._default_manager.filter().delete()
        PassageModel._default_manager.filter().delete()

        for i in range(count):
            suit = SuitFactory()

            count_questions = random.randint(0, SuitModel.MAX_COUNT_QUESTIONS_FOR_COMPLETED_SUIT)
            for j in range(count_questions):
                question = QuestionFactory(suit=suit)

                count_variants = random.randint(0, QuestionModel.MAX_COUNT_VARIANTS_FOR_FULL_QUESTION)
                for k in range(count_variants):
                    VariantFactory(question=question)

            exists_count_questions = suit.questions.count()
            if SuitModel.MIN_COUNT_QUESTIONS_FOR_COMPLETED_SUIT <=\
                    exists_count_questions <= SuitModel.MAX_COUNT_QUESTIONS_FOR_COMPLETED_SUIT:
                suit.status = random.choice([True, False])
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
                QuestionModel._default_manager.count(),
                VariantModel._default_manager.count(),
                PassageModel._default_manager.count(),
            )
        )
