
from django.db import models

from apps.accounts.models import Account


class PollManager(models.Manager):
    """
    Manager for polls
    """

    def close_poll(self, poll):
        """ """

        raise NotImplementedError

    def open_poll(self, poll):
        """ """

        raise NotImplementedError

    def make_poll_as_draft(self, poll):
        """ """

        raise NotImplementedError

    def most_activity_voters(self):
        """A users participated in more than haft from all count polls."""

        half_count_polls = self.count() // 2
        accounts_with_count_votes = Account.objects.accounts_with_count_votes()
        return accounts_with_count_votes.filter(count_votes__gt=half_count_polls)

    def get_all_voters(self):
        """ """

        accounts_with_count_votes = Account.objects.accounts_with_count_votes()
        return accounts_with_count_votes.filter(count_votes__gt=0)
