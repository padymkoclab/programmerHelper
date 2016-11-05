
from django.contrib.contenttypes.models import ContentType
from django.db import models


class OpinionQuerySet(models.QuerySet):

    def objects_with_count_opinions(self):
        """ """

        return self.annotate(count_opinions=models.Count('opinions', distinct=True))


class UserOpinionQuerySet(models.QuerySet):
    """

    """

    def users_with_count_opinions_on_answers_other_users(self):

        from apps.questions.models import Answer

        return self.annotate(
            count_opinions_on_answers_other_users=models.Sum(
                models.Case(
                    models.When(opinions__content_type_id=ContentType.objects.get_for_model(Answer).pk, then=1),
                    output_field=models.PositiveIntegerField()
                )
            )
        )

    def users_with_count_opinions_on_questions_other_users(self):

        from apps.questions.models import Question

        return self.annotate(
            count_opinions_on_questions_other_users=models.Sum(
                models.Case(
                    models.When(opinions__content_type_id=ContentType.objects.get_for_model(Question).pk, then=1),
                    output_field=models.PositiveIntegerField()
                )
            )
        )

    def users_with_count_opinions_on_solutions_other_users(self):

        from apps.solutions.models import Solution

        return self.annotate(
            count_opinions_on_solutions_other_users=models.Sum(
                models.Case(
                    models.When(opinions__content_type_id=ContentType.objects.get_for_model(Solution).pk, then=1),
                    output_field=models.PositiveIntegerField()
                )
            ),
        )

    def users_with_count_opinions_on_utilities(self):

        from apps.utilities.models import Utility

        return self.annotate(
            count_opinions_on_utilities=models.Sum(
                models.Case(
                    models.When(opinions__content_type_id=ContentType.objects.get_for_model(Utility).pk, then=1),
                    output_field=models.PositiveIntegerField()
                )
            )
        )

    def users_with_count_opinions_on_snippets_other_users(self):

        from apps.snippets.models import Snippet

        return self.annotate(
            count_opinions_on_snippets_other_users=models.Sum(
                models.Case(
                    models.When(opinions__content_type_id=ContentType.objects.get_for_model(Snippet).pk, then=1),
                    output_field=models.PositiveIntegerField()
                )
            ),
        )

    def users_with_total_count_opinions(self):

        return self.annotate(total_count_opinions=models.Count('opinions', distinct=True))

    def users_with_date_latest_opinion(self):

        return self.annotate(date_latest_opinion=models.Max('opinions__created'))

    def users_with_count_opinions_on_related_objects_and_total_and_date_latest_opinion(self):

        self = self.users_with_count_opinions_on_answers_other_users()
        self = self.users_with_count_opinions_on_questions_other_users()
        self = self.users_with_count_opinions_on_solutions_other_users()
        self = self.users_with_count_opinions_on_snippets_other_users()
        self = self.users_with_count_opinions_on_utilities()
        self = self.users_with_total_count_opinions()
        self = self.users_with_date_latest_opinion()

        return self
