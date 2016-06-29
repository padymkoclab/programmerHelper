
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

    def polls_with_count_votes(self):
        """Determining count a votes for each poll in a queryset."""

        return self.annotate(count_votes=models.Count('votes', distinct=True))

    def polls_with_count_choices(self):
        """Determining count a votes for each poll in a queryset."""

        return self.annotate(count_choices=models.Count('choices', distinct=True))

    def polls_with_count_choices_and_votes(self):
        """Return the queryset, where each a poll has deternimed a count choices and votes itself."""

        self = self.polls_with_count_votes()
        self = self.polls_with_count_choices()
        return self

    def polls_with_high_activity(self):
        """Polls with equal or great then 30 voters."""

        self = self.polls_with_count_votes()
        return self.filter(count_votes__gte=30)

    def polls_with_low_activity(self):
        """Polls with less then 5 voters."""

        self = self.polls_with_count_votes()
        return self.filter(count_votes__lt=5)


class ChoiceQuerySet(models.QuerySet):
    """
    Queryset for choices
    """

    def choices_with_count_votes(self):
        """Return the queryset where each a choice have determined count a votes."""

        return self.annotate(count_votes=models.Count('votes', distinct=True))
