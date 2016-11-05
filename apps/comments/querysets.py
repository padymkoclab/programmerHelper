
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommentQuerySet(models.QuerySet):

    def objects_with_count_comments(self):
        """Added to each snippet new field with count of comments of the a each snippet."""

        return self.annotate(count_comments=models.Count('comments', distinct=True))


class UserCommentQuerySet(models.QuerySet):
    """

    """

    def users_with_total_count_comments(self):

        return self.annotate(total_count_comments=models.Count('comments', distinct=True))

    def users_with_date_latest_comment(self):

        return self.annotate(date_latest_comment=models.Max('comments__created'))

    def users_with_count_comments_on_articles(self):

        from apps.articles.models import Article

        return self.annotate(
            count_comments_on_articles_other_users=models.functions.Coalesce(
                models.Sum(
                    models.Case(
                        models.When(comments__content_type_id=ContentType.objects.get_for_model(Article).pk, then=1),
                        output_field=models.IntegerField(),
                    )
                ), 0
            )
        )

    def users_with_count_comments_on_snippets(self):

        from apps.snippets.models import Snippet

        return self.annotate(
            count_comments_on_snippets_other_users=models.functions.Coalesce(
                models.Sum(
                    models.Case(
                        models.When(comments__content_type_id=ContentType.objects.get_for_model(Snippet).pk, then=1),
                        output_field=models.IntegerField(),
                    )
                ), 0
            )
        )

    def users_with_count_comments_on_solutions(self):

        from apps.solutions.models import Solution

        return self.annotate(
            count_comments_on_solutions_other_users=models.functions.Coalesce(
                models.Sum(
                    models.Case(
                        models.When(comments__content_type_id=ContentType.objects.get_for_model(Solution).pk, then=1),
                        output_field=models.IntegerField(),
                    )
                ), 0
            )
        )

    def users_with_count_comments_on_utilities(self):

        from apps.utilities.models import Utility

        return self.annotate(
            count_comments_on_utilities=models.functions.Coalesce(
                models.Sum(
                    models.Case(
                        models.When(comments__content_type_id=ContentType.objects.get_for_model(Utility).pk, then=1),
                        output_field=models.IntegerField(),
                    )
                ), 0
            )
        )

    def users_with_count_comments_on_answers(self):

        from apps.questions.models import Answer

        return self.annotate(
            count_comments_on_answers_other_users=models.functions.Coalesce(
                models.Sum(
                    models.Case(
                        models.When(comments__content_type_id=ContentType.objects.get_for_model(Answer).pk, then=1),
                        output_field=models.IntegerField(),
                    )
                ), 0
            )
        )

    def users_with_count_comments_on_its_related_objects_and_total_and_date_latest_comment(self):

        self = self.users_with_total_count_comments()
        self = self.users_with_date_latest_comment()
        self = self.users_with_count_comments_on_articles()
        self = self.users_with_count_comments_on_snippets()
        self = self.users_with_count_comments_on_solutions()
        self = self.users_with_count_comments_on_utilities()
        self = self.users_with_count_comments_on_answers()

        return self
