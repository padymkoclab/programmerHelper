
import itertools
import collections

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import BaseUserManager

from mylabour.utils import get_random_objects
from apps.app_testing.models import TestingPassage


class AccountQuerySet(models.QuerySet):
    """Queryset for processing queryset of model Account."""

    def accounts_with_total_scope_for_solutions(self, queryset=None):
        """Created new field 'total_scope_for_solutions' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""
        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_scope_for_solutions=models.Sum(
                models.Case(
                    models.When(solutions__opinions__is_useful=True, then=1),
                    models.When(solutions__opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def accounts_with_total_scope_for_questions(self, queryset=None):
        """Created new field 'total_scope_for_questions' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""
        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_scope_for_questions=models.Sum(
                models.Case(
                    models.When(questions__opinions__is_useful=True, then=1),
                    models.When(questions__opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def accounts_with_total_scope_for_answers(self, queryset=None):
        """Created new field 'total_scope_for_answers' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""
        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_scope_for_answers=models.Sum(
                models.Case(
                    models.When(answers__likes__liked_it=True, then=1),
                    models.When(answers__likes__liked_it=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    def accounts_with_total_scope_for_snippets(self, queryset=None):
        """Created new field 'total_scope_for_snippets' by help annotation and
         return new queryset for certain instance/instances or all instances, if queryset is none."""
        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(
            total_scope_for_snippets=models.Sum(
                models.Case(
                    models.When(snippets__opinions__is_useful=True, then=1),
                    models.When(snippets__opinions__is_useful=False, then=-1),
                    output_field=models.IntegerField()
                )
            )
        )

    # def accounts_with_total_rating_for_articles(self, queryset=None):
    #     """Created new field 'total_rating_for_articles' by help annotation and
    #      return new queryset for certain instance/instances or all instances, if queryset is none."""
    #     # if queryset is none, then using all instances of model
    #     if queryset is None:
    #         queryset = self
    #     return Article.objects.articles_with_rating().filter(author=self).aggregate(
    #         total_rating_for_articles=models.Sum('rating')
    #     )['total_rating_for_articles']
    #     return queryset.annotate(rating=models.Avg('articles__scopes__scope'))

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

    def objects_with_count_scopes(self, queryset=None):
        """Annotation for getting count scopes on based queryset or all instances."""
        # if queryset is none, then using all instances of model
        if queryset is None:
            queryset = self
        return queryset.annotate(count_opinions=models.Count('scopes', distinct=True))

    def random_accounts(self, count=1):
        """Getting certain count random objects from queryset."""
        return get_random_objects(queryset=self, count=count)

    def objects_with_count_favorites_and_unfavorites(self, queryset=None):
        """Getting count favorites and unfavorites of accounts."""
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
        """Getting count articles of accounts."""
        return self.annotate(count_articles=models.Count('articles', distinct=True))

    def objects_passages_testsuits(self, queryset=None):
        """Getting accounts what passed at least 1 testing suit."""
        return self.filter(passages__status=TestingPassage.CHOICES_STATUS.passed)

    def creators_testing_suits(self):
        """Getting accounts what passed at least 1 testing suit."""
        return self.filter(testing_suits__isnull=False)

    def objects_with_badge(self, badge_name):
        result = self.filter()
        for obj in self.iterator():
            if not obj.has_badge(badge_name):
                result = result.exclude(pk=obj.pk)
        return result


class AccountManager(BaseUserManager):
    """
    Custom manager for custom auth model - Account.
    """

    def create_user(self, email, username, date_birthday, password=None):
        """Create staff user with certain attributes."""

        if not (email, username, date_birthday):
            raise ValueError(_('User must be have email, first name and last name.'))
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            date_birthday=date_birthday,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, date_birthday, password):
        """Creating superuser with certain attributes."""

        user = self.create_user(
            email=email,
            username=username,
            date_birthday=date_birthday,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_filled_accounts_profiles(self, queryset=None):
        """Return in percents, how many filled profiles of accounts information.
        If given queryset, then using its as restriction for selection."""

        result = dict()
        # if queryset is none, then using all instances of models
        if queryset is None:
            queryset = self
        # listing restrictions determinating filled profile of account
        list_restictions = (
                queryset.exclude(presents_on_stackoverflow='').values_list('pk', flat=True),
                queryset.exclude(personal_website='').values_list('pk', flat=True),
                queryset.exclude(presents_on_github='').values_list('pk', flat=True),
                queryset.exclude(presents_on_gmail='').values_list('pk', flat=True),
                queryset.filter(gender__isnull=False).values_list('pk', flat=True),
                queryset.exclude(real_name='').values_list('pk', flat=True),
        )
        # counter all suitable instances
        counter = collections.Counter(
            itertools.chain(*list_restictions)
        )
        # determinating percent filled profile of account
        for pk, value in counter.items():
            result[pk] = 100 / len(list_restictions) * value
        # return as dictioinary {instance.pk: percent}
        return result
