
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils import timezone

from dateutil.relativedelta import relativedelta


class ListFilterLastLogin(admin.SimpleListFilter):
    """
    ListFilter for using in admin on model of users. Namely on field 'last login'.
    """

    title = _('Last login')
    parameter_name = 'last_login'

    def lookups(self, request, model_admin):
        return (
            ('past_hour', _('Past hour')),
            ('past_12_hours', _('Past 12 hours')),
            ('past_24_hours', _('Past 24 hours')),
            ('past_2_days', _('Past 2 days')),
            ('past_week', _('Past week')),
            ('past_month', _('Past month')),
            ('more_year_ago', _('More year ago')),
            ('never', _('Never')),
        )

    def queryset(self, request, queryset):
        tonow = timezone.now()
        if self.value() == 'past_hour':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(hours=1))
        elif self.value() == 'past_12_hours':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(days=0.5))
        elif self.value() == 'past_24_hours':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(days=1))
        elif self.value() == 'past_2_days':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(days=2))
        elif self.value() == 'past_week':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(weeks=1))
        elif self.value() == 'past_month':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(days=30))
        elif self.value() == 'more_year_ago':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(days=365))
        elif self.value() == 'never':
            return queryset.filter(last_login__isnull=True)


class LatestActivityListFilter(admin.SimpleListFilter):
    """
    ListFilter on custom method get_latest_activity.
    """

    title = _('latest activity')
    parameter_name = 'latest_activity'

    def lookups(self, request, model_admin):
        return (
            ('past_hour', _('Past hour')),
            ('past_24_hours', _('Past 24 hours')),
            ('past_2_days', _('Past 2 days')),
            ('past_week', _('Past week')),
            ('past_month', _('Past month')),
            ('more_year_ago', _('More year ago')),
        )

    def queryset(self, request, queryset):
        queryset = queryset.categories_with_count_solutions_total_scope_and_latest_activity()
        tonow = timezone.now()
        if self.value() == 'past_hour':
            return queryset.filter(latest_activity__gte=tonow - timezone.timedelta(hours=1))
        elif self.value() == 'past_24_hours':
            return queryset.filter(latest_activity__gte=tonow - timezone.timedelta(days=1))
        elif self.value() == 'past_2_days':
            return queryset.filter(latest_activity__gte=tonow - timezone.timedelta(days=2))
        elif self.value() == 'past_week':
            return queryset.filter(latest_activity__gte=tonow - timezone.timedelta(weeks=1))
        elif self.value() == 'past_month':
            return queryset.filter(latest_activity__gte=tonow - timezone.timedelta(days=30))
        elif self.value() == 'more_year_ago':
            return queryset.filter(latest_activity__gte=tonow - timezone.timedelta(days=365))
