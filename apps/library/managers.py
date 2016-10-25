
from django.utils.encoding import force_str
from django.db import models
from django.utils.translation import ugettext_lazy as _

import pygal

from utils.django.functions_db import Round

from .querysets import BookQuerySet, PublisherQuerySet, WriterQuerySet


class BookManager(models.Manager):

    def get_count_russian_books(self):
        """ """

        return self.books_wrote_on_russian().count()

    def get_count_english_books(self):
        """ """

        return self.books_wrote_on_english().count()

    def get_count_great_books(self):
        """ """

        return self.get_great_books().count()

    def get_count_big_books(self):
        """ """

        return self.get_big_books().count()

    def get_count_middle_books(self):
        """ """

        return self.get_middle_books().count()

    def get_count_tiny_books(self):
        """ """

        return self.get_tiny_books().count()

    def get_statistics_count_books_by_size(self):
        """ """

        return dict(
            great=self.get_count_great_books(),
            big=self.get_count_big_books(),
            middle=self.get_count_middle_books(),
            tiny=self.get_count_tiny_books(),
        )

    def get_chart_statistics_count_books_by_size(self):
        """ """

        stat_data = self.get_statistics_count_books_by_size()

        config = pygal.Config()
        config.height = 250
        config.legend_at_bottom = True
        config.legend_at_bottom_columns = 4
        config.show_legend = True
        config.spacing = 10

        chart = pygal.HorizontalBar(config)

        chart.add(force_str(_('Great books')), stat_data['great'])
        chart.add(force_str(_('Big books')), stat_data['big'])
        chart.add(force_str(_('Middle books')), stat_data['middle'])
        chart.add(force_str(_('Tiny books')), stat_data['tiny'])

        return chart.render()


class WriterManager(models.Manager):

    def get_avg_count_books(self):
        """ """

        self = self.writers_with_count_books()

        return self.aggregate(avg=Round(
            models.functions.Coalesce(models.Avg('count_books'), 0)
        ))['avg']


class PublisherManager(models.Manager):

    def get_avg_count_books(self):
        """ """

        self = self.publishers_with_count_books()
        return self.aggregate(avg=Round(
            models.functions.Coalesce(models.Avg('count_books'), 0)
        ))['avg']


BookManager = BookManager.from_queryset(BookQuerySet)
WriterManager = WriterManager.from_queryset(PublisherQuerySet)
PublisherManager = PublisherManager.from_queryset(WriterQuerySet)
