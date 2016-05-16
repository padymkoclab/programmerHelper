
from django.db import models


class PollQuerySet(models.QuerySet):
    """

    """

    pass


class VoteInPollManager(models.Manager):
    """
    Model manager
    """

    def all_voters(self):
        return self.values_list('user', flat=True).distinct()
