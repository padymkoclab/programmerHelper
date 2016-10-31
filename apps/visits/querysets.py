
from django.db import models


class AttendanceQuerySet(models.QuerySet):
    """

    """

    def objects_with_count_visitors(self):
        """Return users satisfied consecutive days of attendances on website."""

        return self.annotate(count_visitors=models.Count('users', distinct=True))


class UserAttendanceQuerySet(models.QuerySet):
    """
    A queryset for a user model as manager
    """

    def users_with_count_attendances(self):

        return self.annotate(count_days_attendance=models.Count('attendances', distinct=True))
