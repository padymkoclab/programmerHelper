
from django.db import models

from .querysets import PollQuerySet


class PollManager(models.Manager):
    """
    Manager for polls
    """

    def close_poll(self, poll):
        raise NotImplementedError

    def open_poll(self, poll):
        raise NotImplementedError

    def make_poll_as_draft(self, poll):
        raise NotImplementedError


class OpendedPollManager(models.Manager):
    """
    Manager for opened polls
    """

    def get_queryset(self):
        return PollQuerySet(self.model, using=self._db)

    def working_with_only_opened_polls(self):
        return self.get_queryset().opened_polls()
        raise NotImplementedError

    def make_poll_as_draft(self, poll):
        raise NotImplementedError


class VoteInPollManager(models.Manager):
    """
    Model manager
    """

    def all_voters(self):
        return self.values_list('user', flat=True).distinct()
