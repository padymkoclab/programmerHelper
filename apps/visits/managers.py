
from django.db import models
from django.utils.translation import ugettext as _

import pygal

from .querysets import AttendanceQuerySet


class AttendanceManager(models.Manager):

    pass


class VisitPageManager(models.Manager):
    """
    Custom manager for working with visits of pages.
    """

    def get_count_visits(self, request):
        """Return count visits by certain url or 0."""

        url_path = request.path_info
        try:
            obj = self.get(url=url_path)
        except self.model.DoesNotExist:
            return 0
        else:
            return obj.count

    def change_url_counter(self, request):

        url_path = request.path_info

        obj, is_created = self.get_or_create(url=url_path)

        if not is_created:
            obj.count += 1
            obj.save()


class VisitUserBrowserManager(models.Manager):
    """

    """

    def get_chart_browsers_of_visitors(self):

        config = pygal.Config(
            pie_half=True,
        )

        chart = pygal.Pie(config)
        chart.title = _('Browsers of visitors')
        for name, user_pks in self.values_list('name', 'user_pks'):
            if user_pks == '':
                count = 0
            else:
                count = len(user_pks.split(','))
            chart.add(name, count)
        return chart.render()


class VisitUserSystemManager(models.Manager):
    """

    """

    def get_chart_systems_of_visitors(self):

        config = pygal.Config(
            pie_half=True,
        )

        chart = pygal.Pie(config)
        chart.title = _('Operation systems of visitors')
        for name, user_pks in self.values_list('name', 'user_pks'):
            if user_pks == '':
                count = 0
            else:
                count = len(user_pks.split(','))
            chart.add(name, count)
        return chart.render()


AttendanceManager = AttendanceManager.from_queryset(AttendanceQuerySet)
