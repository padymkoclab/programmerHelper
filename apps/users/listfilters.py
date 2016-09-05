
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class DecadeBornListFilter(admin.SimpleListFilter):
    """
    A ListFilter for filter a users by decade born of year, on based date birth of each user.
    """

    title = _('Decade born')

    def lookups(self):
        return (
            ('', _('Born in the summer')),
            ('', _('Born in the winter')),
            ('', _('Born in the autumn')),
            ('', _('Born in the spring')),
        )

    def queryset(self, request, queryset):
        if self.values() == '':
            return


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
