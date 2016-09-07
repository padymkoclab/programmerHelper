
from django.db import models


class SuitQuerySet(models.QuerySet):

    def suit_with_count_questions(self):
        """ """

        return self.annotate(count_questions=models.Count('questions', distinct=True))

    def suits_with_all_additional_fields(self):
        """ """

        self = self.suit_with_count_questions()

        return self


class TestQuestionQuerySet(models.QuerySet):

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
