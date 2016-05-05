
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils import timezone


class ListFilterLastLogin(admin.SimpleListFilter):
    title = _('Last login')
    parameter_name = 'last_login'

    def lookups(self, request, model_admin):
        return (
            ('past_hour', _('Past hour')),
            ('past_12_hours', _('Past 12 hours')),
            ('past_24_hours', _('Past 24 hours')),
            ('yesterday', _('Yesterday')),
            ('past_7_days', _('Past 7 days')),
            ('past_month', _('Past month')),
            ('past_year', _('Past year')),
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
        elif self.value() == 'yesterday':
            return queryset.filter(last_login__range=(tonow - timezone.timedelta(days=2), (tonow - timezone.timedelta(days=1))))
        elif self.value() == 'past_7_days':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(weeks=1))
        elif self.value() == 'past_month':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(days=30))
        elif self.value() == 'past_year':
            return queryset.filter(last_login__gte=tonow - timezone.timedelta(days=256))
        elif self.value() == 'never':
            return queryset.filter(last_login__isnull=True)
