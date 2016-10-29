
from django.db import models


class AttendanceQuerySet(models.QuerySet):
    """

    """

    def objects_with_count_visitors(self):
        """Return users satisfied consecutive days of attendances on website."""

        return self.annotate(count_visitors=models.Count('users', distinct=True))
