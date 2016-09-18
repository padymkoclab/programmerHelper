
import collections

from django.db import models

import pygal

from utils.django.functions_db import Round

from .querysets import MarkQuerySet


class MarkManager(models.Manager):
    """

    """

    def get_total_count_marks(self):
        """ """

        self = self.objects_with_count_marks()
        return self.aggregate(sum=models.Sum('count_marks'))['sum']

    def get_avg_count_marks_on_object(self):
        """ """

        self = self.objects_with_count_marks()
        return self.aggregate(avg=Round(
            models.functions.Coalesce(models.Avg('count_marks'), 0)
        ))['avg']

    def get_statistics_used_marks(self):
        """Return count a used tags on deternimed type objects."""

        marks = self.filter(marks__mark__isnull=False).values_list('marks__mark', flat=True)

        counter_marks = collections.Counter(marks)

        stat = [(mark, count) for mark, count in counter_marks.items()]

        stat.sort(key=lambda x: x[0])

        return stat

    def get_chart_used_marks(self):
        """ """

        stat = self.get_statistics_used_marks()

        config = pygal.Config(
            width=800,
            height=300,
            explicit_size=True,
            legend_box_size=5,
        )

        chart = pygal.HorizontalBar(config)

        for mark, count in stat:
            chart.add(str(mark), count)

        return chart.render()


MarkManager = MarkManager.from_queryset(MarkQuerySet)
