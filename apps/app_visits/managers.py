
from django.db import models


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
