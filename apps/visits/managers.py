
from django.db import models

from .querysets import AttendanceQuerySet


class AttendanceManager(models.Manager):

    pass


class VisitPageManager(models.Manager):
    """
    Custom manager for working with visits of pages.
    """

    def get_count_visits(self, request):
        """Return count visits by certain url or 0."""

        url_path = request.path_info
        try:
            obj = self.get(url=url_path)
        except self.model.DoesNotExist:
            return 0
        else:
            return obj.count

    def change_url_counter(self, request):

        url_path = request.path_info

        obj, is_created = self.get_or_create(url=url_path)

        if not is_created:
            obj.count += 1
            obj.save()


AttendanceManager = AttendanceManager.from_queryset(AttendanceQuerySet)
