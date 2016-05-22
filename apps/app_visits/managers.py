
from django.db import models


class DayAttendanceQuerySet(models.QuerySet):
    """

    """

    def objects_by_count_consecutive_days(self, consecutive_days):
        """Return users satisfied consecutive days of attendances on website."""
        return self.order_by('day_attendance').annotate()


class VisitManager(models.Manager):
    """
    Custom manager for working with visits of pages.
    """

    def get_count_visits_by_url(self, url):
        """Return count visits by certain url or 0."""
        try:
            count = self.get(url=url).users.count()
        except self.model.DoesNotExist:
            count = 0
        return count
