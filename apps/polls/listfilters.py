
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from utils.django.listfilters import DatetimeWithNullSimpleListFilter


class IsActiveVoterListFilter(admin.SimpleListFilter):
    """ """

    title = _('Is active voter')
    parameter_name = 'is_active_voter'

    def lookups(self, request, model_admin):
        """ """

        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, qs):
        """ """

        if self.value() == 'yes':
            return qs.filter(is_active_voter=True)
        elif self.value() == 'no':
            return qs.filter(is_active_voter=False)
        else:
            return qs


class LatestVotingSimpleListFilter(DatetimeWithNullSimpleListFilter):

    title = 'Date latest voting'
    parameter_name = 'date_latest_voting'
    field_for_lookup = 'date_latest_voting'
