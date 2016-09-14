
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.listfilters import DatetimeSimpleListFilter


class HasAcceptedAnswerSimpleListFilter(admin.SimpleListFilter):

    title = _('Has accepted answer?')
    parameter_name = 'has_accepted_answer'

    def lookups(self, request, model_admin):

        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter(_has_accepted_answer=True)
        elif self.value() == 'no':
            return queryset.filter(_has_accepted_answer=False)


class LatestActivitySimpleListFilter(DatetimeSimpleListFilter):

    title = _('Date latest activity')
    parameter_name = 'latest_activity'
    field_for_lookup = 'date_latest_activity'
