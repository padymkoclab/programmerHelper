
from django.db import models


class AttendanceQuerySet(models.QuerySet):
    """

    """

    def objects_by_count_consecutive_days(self, consecutive_days):
        """Return users satisfied consecutive days of attendances on website."""
        return self.order_by('day_attendance').annotate()
