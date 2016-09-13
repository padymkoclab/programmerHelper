
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


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


class LatestActivitySimpleListFilter(admin.SimpleListFilter):

    title = _('Latest activity')
    parameter_name = 'has_accepted_answer'

    def lookups(self, request, model_admin):

        return (
            ('today', _('Today')),
            ('week', _('Past 7 days')),
            ('month', _('This month')),
            ('year', _('This year')),
        )

    def queryset(self, request, queryset):

        now = timezone.now()

        date_ago = None

        if self.value() == 'today':
            date_ago = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.value() == 'week':
            date_ago = now - timezone.timedelta(days=7)
        if self.value() == 'month':
            date_ago = now.replace(day=1)
        if self.value() == 'year':
            date_ago = now.replace(month=1, day=1)

        if date_ago is not None:
            return queryset.filter(date_latest_activity__gte=date_ago)
