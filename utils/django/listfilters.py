
import datetime

from django.utils.encoding import smart_text
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils import timezone
from django.conf import settings

from dateutil.relativedelta import relativedelta


class AllValuesChoicesFieldListFilter(admin.AllValuesFieldListFilter):

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None and self.lookup_val_isnull is None,
            'query_string': changelist.get_query_string({}, [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        include_none = False

        # all choices for this field
        choices = dict(self.field.choices)

        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue
            val = smart_text(val)
            yield {
                'selected': self.lookup_val == val,
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg: val,
                }, [self.lookup_kwarg_isnull]),

                # instead code, display title
                'display': choices[val],
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }


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


class IsNewSimpleListFilter(admin.SimpleListFilter):

    title = _('Is new?')
    parameter_name = 'is_new'

    def lookups(self, request, model_admin):

        return [
            ('new', _('New')),
            ('no_new', _('No new')),
        ]

    def queryset(self, request, queryset):

        date_ago = timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_FOR_NEW_ELEMENTS)

        if self.value() == 'new':
            return queryset.filter(date_added__gte=date_ago)
        elif self.value() == 'no_new':
            return queryset.exclude(date_added__gte=date_ago)


class RangeSimpleListFilter(admin.ListFilter):
    # The parameter that should be used in the query string for that filter.
    parameter_name = None

    def __init__(self, request, params, model, model_admin):
        super(RangeSimpleListFilter, self).__init__(
            request, params, model, model_admin)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify "
                "a 'parameter_name'." % self.__class__.__name__)
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value
        lookup_choices = self.lookups(request, model_admin)
        if lookup_choices is None:
            lookup_choices = ()
        self.lookup_choices = list(lookup_choices)

    def has_output(self):
        return len(self.lookup_choices) > 0

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name)

    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError(
            'The RangeSimpleListFilter.lookups() method must be overridden to '
            'return a list of tuples (value, verbose value)')

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, cl):
        yield {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }


class DateRangeFieldListFilter(admin.FieldListFilter):

    template = 'mylabour/range_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):

        self.field_generic_lookup = '%s__' % field_path

        self.lookup_kwarg_since = '%s__range_gte' % field_path
        self.lookup_kwarg_until = '%s__range_lt' % field_path

        super(DateRangeFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_until]

    def choices(self, cl):
        raise NotImplementedError('Not worked URL replace')
        return (
            # '1', '2', '3'
            # (1, 'start_date', 2),
            # (2, 'end_date', 2),
        )

    def queryset(self, request, qs):

        # remove keys with empty values
        self.used_parameters = {k: v for k, v in self.used_parameters.items() if v}

        # replace key name on corresponding for filter in Django ORM
        self.used_parameters = {k.replace('range_', ''): v for k, v in self.used_parameters.items()}

        # make filter by parameters, if is
        return qs.filter(**self.used_parameters)


admin.FieldListFilter.register(lambda f: isinstance(f, models.DateField), DateRangeFieldListFilter)


class DatetimeSimpleListFilter(admin.SimpleListFilter):

    def lookups(self, request, model_admin):

        return [
            ('today', _('Today')),
            ('week', _('Past 7 days')),
            ('month', _('This month')),
            ('year', _('This year')),
        ]

    def queryset(self, request, queryset):

        condititons = self._get_conditions()

        if condititons is not None:
            return queryset.filter(**condititons)

    def _get_conditions(self):
        """ """

        now = timezone.now()

        date_ago = None
        condititons = None

        if self.value() == 'today':
            date_ago = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.value() == 'week':
            date_ago = now - timezone.timedelta(days=7)
        if self.value() == 'month':
            date_ago = now.replace(day=1)
        if self.value() == 'year':
            date_ago = now.replace(month=1, day=1)

        if date_ago is not None:
            condititons = {self.field_for_lookup + '__gte': date_ago}

        return condititons


class DatetimeWithNullSimpleListFilter(DatetimeSimpleListFilter):

    def lookups(self, request, model_admin):

        lookups = super().lookups(request, model_admin)
        lookups.append(
            ('never', _('Never')),
        )
        return lookups

    def _get_conditions(self):

        conditions = super()._get_conditions()

        if self.value() == 'never':
            conditions = {self.field_for_lookup + '__isnull': True}

        return conditions
