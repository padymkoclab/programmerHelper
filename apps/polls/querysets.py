
from django.db import models


class PollQuerySet(models.QuerySet):
    """
    Additional methods for queryset of polls
    """

    def opened_polls(self):
        """Return only polls where status is opened"""

        return self.filter(status=self.model.CHOICES_STATUS.opened)

    def closed_polls(self):
        """Return only polls where status is closed"""

        return self.filter(status=self.model.CHOICES_STATUS.closed)

    def draft_polls(self):
        """Return only polls where status is draft"""

        return self.filter(status=self.model.CHOICES_STATUS.draft)

    def polls_with_high_activity(self):
        """Polls with equal or great then 30 voters."""

        raise NotImplementedError

    def polls_with_low_activity(self):
        """Polls with less then 5 voters."""

        raise NotImplementedError
