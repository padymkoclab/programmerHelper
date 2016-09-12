
from django.db import models

from utils.python.logging_utils import create_logger_by_filename
from utils.django.models_utils import get_random_objects

logger = create_logger_by_filename(__name__)


class UserQuerySet(models.QuerySet):
    """
    Queryset for users.
    """

    def active_users(self):
        """Filter only active user."""

        return self.filter(is_active=True)

    def non_active_users(self):
        """Filter only non active user."""

        return self.filter(is_active=False)

    def superusers(self):
        """Filter only superusers."""

        return self.filter(is_superuser=True)

    def users_with_total_mark_for_solutions(self, queryset=None):
        """Created new field 'total_mark_for_solutions' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_mark_for_solutions=models.Sum(
                models.Case(
                    models.When(solutions__opinions__is_useful=True, then=1),
                    models.When(solutions__opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def users_with_total_mark_for_questions(self, queryset=None):
        """Created new field 'total_mark_for_questions' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_mark_for_questions=models.Sum(
                models.Case(
                    models.When(questions__opinions__is_useful=True, then=1),
                    models.When(questions__opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def users_with_total_mark_for_answers(self, queryset=None):
        """Created new field 'total_mark_for_answers' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_mark_for_answers=models.Sum(
                models.Case(
                    models.When(answers__likes__liked_it=True, then=1),
                    models.When(answers__likes__liked_it=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def users_with_total_mark_for_snippets(self, queryset=None):
        """Created new field 'total_mark_for_snippets' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_mark_for_snippets=models.Sum(
                models.Case(
                    models.When(snippets__opinions__is_useful=True, then=1),
                    models.When(snippets__opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    # def users_with_total_rating_for_articles(self, queryset=None):
    #     """Created new field 'total_rating_for_articles' by help annotation and
    #      return new queryset for certain instance/instances or all instances, if queryset is none."""
    #     # if queryset is none, then using all instances of model
    #     if queryset is None:
    #         queryset = self
    #     return Article.objects.articles_with_rating().filter(author=self).aggregate(
    #         total_rating_for_articles=models.Sum('rating')
    #     )['total_rating_for_articles']
    #     return queryset.annotate(rating=models.Avg('articles__marks__mark'))

    def objects_with_count_opinions(self, queryset=None):
        """Annotation for getting count opinions on based queryset or all instances."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(count_opinions=models.Count('opinions', distinct=True))

    def objects_with_count_comments(self, queryset=None):
        """Annotation for getting count comments on based queryset or all instances."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(count_opinions=models.Count('comments', distinct=True))

    def objects_with_count_likes(self, queryset=None):
        """Annotation for getting count likes on based queryset or all instances."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(count_opinions=models.Count('likes', distinct=True))

    def objects_with_count_marks(self, queryset=None):
        """Annotation for getting count marks on based queryset or all instances."""

        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(count_opinions=models.Count('marks', distinct=True))

    def random_users(self, count, single_as_qs=False):
        """Getting certain count random objects from queryset."""

        return get_random_objects(queryset=self, count=count, single_as_qs=single_as_qs)

    def objects_with_count_favorites_and_unfavorites(self, queryset=None):
        """Getting count favorites and unfavorites of users."""

        return self.annotate(
            count_favorites=models.Sum(
                models.Case(
                    models.When(opinions__is_favorite=True, then=1),
                    output_field=models.IntegerField()
                ),
            ),
            count_unfavorites=models.Sum(
                models.Case(
                    models.When(opinions__is_favorite=False, then=1),
                    output_field=models.IntegerField()
                ),
            )
        )

    def objects_with_count_articles(self, queryset=None):
        """Getting count articles of users."""

        return self.annotate(count_articles=models.Count('articles', distinct=True))

    def objects_passages_testsuits(self, queryset=None):
        """Getting users what passed at least 1 testing suit."""

        logger.debug('Temp does not working')
        return self.filter(passages__status=Passage.CHOICES_STATUS.passed)

    def creators_testing_suits(self):
        """Getting users what passed at least 1 testing suit."""

        return self.filter(testing_suits__isnull=False)

    def objects_with_badge(self, badge_name):

        result = self.filter()
        for obj in self.iterator():
            if not obj.has_badge(badge_name):
                result = result.exclude(pk=obj.pk)
        return result

    def users_with_count_votes(self):
        """Return queryset where to determined count votes for each user."""

        return self.annotate(count_votes=models.Count('votes', distinct=True))
