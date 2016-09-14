
from django.utils.translation import ugettext as _
from django.db import models

import pygal

from utils.django.functions_db import Round

from apps.core.utils import get_statistics_count_objects_for_the_past_year


class SuitManager(models.Manager):
    """

    """

    def get_avg_count_passages(self):
        """ """

        self = self.suits_with_count_passages()
        avg = self.aggregate(avg=Round(models.Avg('count_passages')))['avg']
        return avg or 0

    def get_avg_count_questions(self):
        """ """

        self = self.suits_with_count_questions()
        avg = self.aggregate(avg=Round(models.Avg('count_questions')))['avg']
        return avg or 0


class QuestionManager(models.Manager):
    """
    Model manager
    """

    def get_avg_count_variants(self):
        """ """

        self = self.questions_with_count_variants()
        avg = self.aggregate(avg=Round(models.Avg('count_variants')))['avg']
        return avg or 0


class PassageManager(models.Manager):
    """
    Model manager
    """

    def get_count_attempt_passages(self):
        """ """

        return self.filter(status=self.model.ATTEMPT).count()

    def get_count_passed_passages(self):
        """ """

        return self.filter(status=self.model.PASSED).count()

    def get_count_distinct_testers(self):
        """ """

        return self.values('user').distinct().count()

    def get_avg_mark_passages(self):
        """ """

        avg = self.aggregate(avg=Round(models.Avg('mark')))['avg']
        return avg or 0

    def get_statistics_count_passages_by_the_past_year(self):
        """ """

        # statistics for all passages
        # unpack it as dates and statistical data for all passages
        dates, stat_total = zip(*get_statistics_count_objects_for_the_past_year(self, 'date'))

        # statistics for passages with status "attempt"
        attempt_passages = self.filter(status=self.model.ATTEMPT)
        stat_attempt = tuple(zip(*get_statistics_count_objects_for_the_past_year(attempt_passages, 'date')))[1]

        # statistics for passages with status "passed"
        passed_passages = self.filter(status=self.model.PASSED)
        stat_passed = tuple(zip(*get_statistics_count_objects_for_the_past_year(passed_passages, 'date')))[1]

        # tuple of tuples (date, total_count, attempt_count, passed_count)
        stat = zip(dates, stat_total, stat_attempt, stat_passed)

        return tuple(stat)

    def get_chart_count_passages_for_the_past_year(self):
        """Return a chart with three lines:
            1. common count passages;
            2. count attempt passages;
            3. count passed passages;
        for the past year.
        """

        # get statistics data
        statistics_count_passages_by_the_past_year = self.get_statistics_count_passages_by_the_past_year()

        # unpack the statdata to dates and values
        dates_labels, *data = zip(*statistics_count_passages_by_the_past_year)

        # unpack the values on three types
        stat_all_passages, stat_atempt_passages, stat_passed_passages = data

        # a config for a chart
        config = pygal.Config()
        config.interpolate = 'cubic'
        config.style = pygal.style.DefaultStyle
        config.show_legend = True
        config.legend_at_bottom = True
        config.legend_at_bottom_columns = 1
        config.fill = False
        config.width = 800
        config.height = 450
        config.margin_bottom = 0
        config.x_labels = dates_labels
        config.x_label_rotation = -50
        config.explicit_size = True

        # create a chart
        chart = pygal.Bar(config)

        # add data
        chart.add(_('Total count passages'), stat_all_passages)
        chart.add(_('Count attempt passages'), stat_atempt_passages)
        chart.add(_('Count passed passages'), stat_passed_passages)

        svg = chart.render()
        return svg
