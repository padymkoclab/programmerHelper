
from django.db import models


class SuitQuerySet(models.QuerySet):

    def suits_with_count_questions(self):
        """ """

        return self.annotate(count_questions=models.Count('questions', distinct=True))

    def suits_with_count_passages(self):
        """ """

        return self.annotate(count_passages=models.Count('passages', distinct=True))

    def suits_with_count_attempt_passages(self):
        """ """

        Warning('Don`t use')

        TestResultModel = self.model.testers.through
        return self.annotate(
            count_attempt_passages=models.Sum(
                models.Case(
                    models.When(passages__status=TestResultModel.ATTEMPT, then=1),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        )

    def suits_with_count_passed_passages(self):
        """ """

        Warning('Don`t use')

        TestResultModel = self.model.testers.through
        return self.annotate(
            count_passed_passages=models.Sum(
                models.Case(
                    models.When(passages__status=TestResultModel.PASSED, then=1),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        )

    def suits_with_avg_marks(self):
        """ """

        raise NotImplementedError

    def suits_with_all_additional_fields(self):
        """ """

        self = self.suits_with_count_questions()
        self = self.suits_with_count_passages()

        return self


class QuestionQuerySet(models.QuerySet):

    def questions_with_count_variants(self):
        """ """

        return self.annotate(count_variants=models.Count('variants', distinct=True))

    def questions_with_status_completeness(self):
        """ """

        return self.questions_with_count_variants().annotate(status_completeness=models.Case(
            models.When(count_variants__range=[
                self.model.MIN_COUNT_VARIANTS_FOR_FULL_QUESTION,
                self.model.MAX_COUNT_VARIANTS_FOR_FULL_QUESTION,
            ], then=True),
            default=False,
            output_field=models.BooleanField()
        ))

    def questions_with_all_additional_fields(self):
        """ """

        # self = self.questions_with_count_variants()
        self = self.questions_with_status_completeness()

        return self
