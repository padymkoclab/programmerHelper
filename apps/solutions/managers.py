
from django.db import models

import pygal

from utils.django.model_utils import get_statistics_count_objects_for_the_past_year as get_statistics


class SolutionManager(models.Manager):
    """
    Model manager for solutions.
    """

    def complain_on_the_solution(self, solution):
        """Complain on the solution sended admin and author corresponding notification."""

        raise NotImplementedError

    def get_statistics_count_solutions_for_the_past_year(self):
        """ """

        return get_statistics(self, 'date_added')

    def get_chart_count_solutions_for_the_past_year(self):
        """ """

        config = pygal.Config()
        config.width = 800
        config.height = 500
        config.explicit_size = True
        config.fill = True
        config.show_legend = False
        config.interpolate = 'hermite'
        config.interpolation_parameters = {'type': 'cardinal', 'c': .75}

        chart = pygal.StackedLine(config)

        statistics = self.get_statistics_count_solutions_for_the_past_year()

        dates, data = zip(*statistics)

        chart.x_labels = dates
        chart.add('Count solutions', data)
        svg = chart.render()
        return svg
