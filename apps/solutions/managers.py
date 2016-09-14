
from django.db import models

from apps.core.utils import (
    get_statistics_count_objects_for_the_past_year,
    get_chart_count_objects_for_the_past_year,
)


class SolutionManager(models.Manager):
    """
    Model manager for solutions.
    """

    def complain_on_the_solution(self, solution):
        """Complain on the solution sended admin and author corresponding notification."""

        raise NotImplementedError

    def get_statistics_count_solutions_for_the_past_year(self):
        """ """

        return get_statistics_count_objects_for_the_past_year(self, 'date_added')

    def get_chart_count_solutions_for_the_past_year(self):
        """ """

        return get_chart_count_objects_for_the_past_year(
            self.get_statistics_count_solutions_for_the_past_year()
        )
