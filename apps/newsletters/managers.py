
from django.db import models

from apps.core.utils import (
    get_statistics_count_objects_for_the_past_year,
    get_chart_count_objects_for_the_past_year,
)


class ManagerNewsletter(models.Manager):
    """
    Model manager
    """

    def get_statistics_count_newsletters_for_the_past_year(self):
        """ """

        return get_statistics_count_objects_for_the_past_year(self, 'date_added')

    def get_chart_count_newsletters_for_the_past_year(self):
        """ """

        return get_chart_count_objects_for_the_past_year(
            self.get_statistics_count_newsletters_for_the_past_year()
        )
