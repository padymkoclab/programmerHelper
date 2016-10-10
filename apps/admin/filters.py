
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from django import template


class BaseFilter(object):

        template = None

        def __init__(self, field_name, field, model, *args, **kwargs):
            self.field_name = field_name
            self.field = field
            self.model = model

            self.title = field.verbose_name

        def queryset(self, request, qs):

            restrictions = dict()
            for expected_parameter in self.expected_parameters:
                value = request.GET.get(expected_parameter)

                if value:
                    restrictions[expected_parameter] = value

            return qs.filter(**restrictions)


class DateTimeRangeFilter(BaseFilter):

    template = 'admin/admin/filters/daterange_filter.html'

    def __init__(self, field_name, field, model, *args, **kwargs):
        super().__init__(field_name, field, model, *args, **kwargs)

        self.lookup_since = self.field_name + '__gte'
        self.lookup_until = self.field_name + '__lt'

    def choices(self, changelist_view):

        now = timezone.now()

        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(self.field, models.DateTimeField):
            now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            now = now.date()

        tomorrow = now + timezone.timedelta(days=1)
        yesterday = now - timezone.timedelta(days=1)

        # start week from Monday and numeration from 1, latest day of week is Sunday with number 7
        now_weekday_number = now.isoweekday()

        start_weekday = now - timezone.timedelta(days=now_weekday_number - 1)
        end_weekday = now + timezone.timedelta(days=7 - now_weekday_number)

        this_month = now.replace(day=1)
        if now.month == 12:
            next_month = now.replace(year=now.year + 1, month=1, day=1)
        else:
            next_month = now.replace(month=now.month + 1, day=1)

        this_year = now.replace(year=now.year, month=1, day=1)
        next_year = now.replace(year=now.year + 1, month=1, day=1)

        return (
            {
                'display_text': _('Any date'),
                'selected': False,
                'querystring': changelist_view.get_querystring(**{
                    self.lookup_since: None,
                    self.lookup_until: None,
                }),
            },
            {
                'display_text': _('Today'),
                'selected': False,
                'querystring': changelist_view.get_querystring(**{
                    self.lookup_since: str(now),
                    self.lookup_until: str(tomorrow),
                }),
            },
            {
                'display_text': _('Yesterday'),
                'selected': False,
                'querystring': changelist_view.get_querystring(**{
                    self.lookup_since: str(yesterday),
                    self.lookup_until: str(end_weekday),
                }),
            },
            {
                'display_text': _('This week'),
                'selected': False,
                'querystring': changelist_view.get_querystring(**{
                    self.lookup_since: str(start_weekday),
                    self.lookup_until: str(tomorrow),
                }),
            },
            {
                'display_text': _('This month'),
                'selected': False,
                'querystring': changelist_view.get_querystring(**{
                    self.lookup_since: str(this_month),
                    self.lookup_until: str(next_month),
                }),
            },
            {
                'display_text': _('This year'),
                'selected': False,
                'querystring': changelist_view.get_querystring(**{
                    self.lookup_since: str(this_year),
                    self.lookup_until: str(next_year),
                }),
            },
        )

    @property
    def expected_parameters(self):

        return (
            self.lookup_since,
            self.lookup_until,
        )

    def get_details(self, request):

        return (
            {
                'label': _('Min'),
                'lookup': self.lookup_since,
                'id': '{}_{}'.format(self.field_name, self.lookup_since),
                'expected_parameter': self.lookup_since,
                'value': request.GET.get(self.lookup_since, ''),
            },
            {
                'label': _('Max'),
                'lookup': self.lookup_until,
                'id': '{}_{}'.format(self.field_name, self.lookup_until),
                'expected_parameter': self.lookup_until,
                'value': request.GET.get(self.lookup_until, ''),
            },
        )


class RelatedOnlyFieldListFilter(BaseFilter):

    template = 'admin/admin/filters/relatedonlyfield_listfilter.html'

    def __init__(self, field_name, field, model, *args, **kwargs):
        super().__init__(field_name, field, model, *args, **kwargs)

        self.lookup_related_field = self.field_name

    @property
    def expected_parameters(self):
        return (self.lookup_related_field, )

    def value(self, request):
        return request.GET.get(self.lookup_related_field, '')

    def choices(self, request):

        pks_related_objects = self.model._base_manager.values(self.field_name)
        choices = self.field.get_choices(
            include_blank=True,
            limit_choices_to={'pk__in': pks_related_objects},
        )

        value = self.value(request)

        choices2 = list()
        for pk, choice in choices:

            is_selected = True if value == str(pk) else False

            choices2.append({
                'value': pk,
                'is_selected': is_selected,
                'text_dislay': choice,
            })
        return choices2

    def get_details(self, request):

        return (
            {
                'expected_parameter': self.lookup_related_field,
                'choices': self.choices(request),
            }
        )
