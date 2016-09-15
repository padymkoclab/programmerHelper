
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class OpinionsModelMixin:

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
