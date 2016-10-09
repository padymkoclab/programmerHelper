
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from django import template


class DateTimeFilter:

    template = 'admin/admin/_/filter.html'

    def __init__(self, field_name, field, model, *args, **kwargs):
        self.field_name = field_name
        self.field = field
        self.model = model

        self.title = field.verbose_name

        self.lookup_since = self.field_name + '__gte'
        self.lookup_until = self.field_name + '__lt'

    def queryset(self):
        return

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

    def expected_parameters(self):

        return (
            self.lookup_since,
            self.lookup_until,
        )
