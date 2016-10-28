
from django.db import models


class BadgeQuerySet(models.QuerySet):
    """

    """

    def last_got_badges(self, count_last_getting=10):
        """Getting listing last getting badges of accounts."""

        pass
