
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class OpinionModelMixin(object):

    def get_count_opinions(self):
        """ """

        if hasattr(self, 'count_opinions'):
            return self.count_opinions

        return self.opinions.count()
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_rating(self):
        """ """

        if hasattr(self, 'rating'):
            return self.rating

        opinions = self.opinions.annotate(is_useful_int=models.Case(
            models.When(is_useful=True, then=1),
            models.When(is_useful=False, then=-1),
            output_field=models.IntegerField(),
        ))

        return opinions.aggregate(rating=models.Sum('is_useful_int'))['rating']
    get_rating.short_description = _('Rating')
    get_rating.admin_order_field = 'rating'

    def get_count_critics(self):
        """Get count good opinions about this snippet."""

        return self.get_critics().count()
    get_count_critics.short_description = _('Count critics')

    def get_count_supporters(self):
        """Get count bad opinions about this snippet."""

        return self.get_supporters().count()
    get_count_supporters.short_description = _('Count supporters')

    def get_critics(self):
        """Return the users determined this snippet as not useful."""

        user = self.opinions.filter(is_useful=False).values('user__pk')
        return get_user_model()._default_manager.filter(pk__in=user)
    get_critics.short_description = _('Critics')

    def get_supporters(self):
        """Return the users determined this snippet as useful."""

        user = self.opinions.filter(is_useful=True).values('user__pk')
        return get_user_model()._default_manager.filter(pk__in=user)
    get_supporters.short_description = _('Supporters')


class UserOpinionModelMixin(object):
    """

    """

    def get_count_opinions_on_questions_other_users(self):

        from apps.questions.models import Question

        if hasattr(self, 'count_opinions_on_questions_other_users'):
            return self.count_opinions_on_questions_other_users

        return self.opinions.filter(content_type=ContentType.objects.get_for_model(Question)).count()
    get_count_opinions_on_questions_other_users.short_description = _('Count opinions on questions')
    get_count_opinions_on_questions_other_users.admin_order_field = 'count_opinions_on_questions_other_users'

    def get_count_opinions_on_solutions_other_users(self):

        from apps.solutions.models import Solution

        if hasattr(self, 'count_opinions_on_solutions_other_users'):
            return self.count_opinions_on_solutions_other_users

        return self.opinions.filter(content_type=ContentType.objects.get_for_model(Solution)).count()
    get_count_opinions_on_solutions_other_users.short_description = _('Count opinions on solutions')
    get_count_opinions_on_solutions_other_users.admin_order_field = 'count_opinions_on_solutions_other_users'

    def get_count_opinions_on_snippets_other_users(self):

        from apps.snippets.models import Snippet

        if hasattr(self, 'count_opinions_on_snippets_other_users'):
            return self.count_opinions_on_snippets_other_users

        return self.opinions.filter(content_type=ContentType.objects.get_for_model(Snippet)).count()
    get_count_opinions_on_snippets_other_users.short_description = _('Count opinions on snippets')
    get_count_opinions_on_snippets_other_users.admin_order_field = 'count_opinions_on_snippets_other_users'

    def get_count_opinions_on_answers_other_users(self):

        from apps.questions.models import Answer

        if hasattr(self, 'count_opinions_on_answers_other_users'):
            return self.count_opinions_on_answers_other_users

        return self.opinions.filter(content_type=ContentType.objects.get_for_model(Answer)).count()
    get_count_opinions_on_answers_other_users.short_description = _('Count opinions on answers')
    get_count_opinions_on_answers_other_users.admin_order_field = 'count_opinions_on_answers_other_users'

    def get_count_opinions_on_utilities(self):

        from apps.utilities.models import Utility

        if hasattr(self, 'count_opinions_on_utilities'):
            return self.count_opinions_on_utilities

        return self.opinions.filter(content_type=ContentType.objects.get_for_model(Utility)).count()
    get_count_opinions_on_utilities.short_description = _('Count opinions on utilities')
    get_count_opinions_on_utilities.admin_order_field = 'count_opinions_on_utilities'

    def get_total_count_opinions(self):
        """ """

        if hasattr(self, 'total_count_opinions'):
            return self.total_count_opinions

        return self.opinions.count()
    get_total_count_opinions.admin_order_field = 'total_count_opinions'
    get_total_count_opinions.short_description = _('Total count opinions')

    def get_date_latest_opinion(self):
        """ """

        if hasattr(self, 'date_latest_opinion'):
            return self.date_latest_opinion

        return self.opinions.aggregate(
            date_latest_opinion=models.Max('created')
        )['date_latest_opinion']
    get_date_latest_opinion.admin_order_field = 'date_latest_opinion'
    get_date_latest_opinion.short_description = _('Latest opinion')
