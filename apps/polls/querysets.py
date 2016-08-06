
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

    def polls_with_date_lastest_voting(self):
        """Return a queryset with determined last voting`s date for an each polls."""

        return self.annotate(date_latest_voting=models.Max('votes__date_voting'))

    def polls_with_count_choices_and_votes_and_date_lastest_voting(self):
        """Return the queryset, where each a poll has deternimed a count choices and votes itself."""

        self = self.polls_with_count_votes()
        self = self.polls_with_count_choices()
        self = self.polls_with_date_lastest_voting()
        self = self.prefetch_related('voters', 'choices', 'votes')
        return self


class ChoiceQuerySet(models.QuerySet):
    """
    Queryset for choices
    """

    def choices_with_count_votes(self):
        """Return the queryset where each a choice have determined count a votes."""

        return self.annotate(count_votes=models.Count('votes', distinct=True))


class UserPollQuerySet(models.QuerySet):
    """ """

    def users_with_count_votes(self):
        """ """

        return self.annotate(count_votes=models.Count('votes', distinct=True))

    def users_with_date_latest_voting(self):
        """ """

        return self.annotate(date_latest_voting=models.Max('votes__date_voting'))

    def users_with_active_voters_status(self):
        """ """

        # make determination of count votes of each user
        self = self.users_with_count_votes()

        # get a half from count polls
        half_from_count_polls = self.model.polls._get_half_from_total_count_polls()

        #
        return self.annotate(is_active_voter=models.Case(
            models.When(count_votes__gt=half_from_count_polls, then=True),
            models.When(count_votes__lte=half_from_count_polls, then=False),
            output_field=models.BooleanField()
        ))

    def users_as_voters(self):
        """ """

        self = self.users_with_date_latest_voting()
        self = self.users_with_active_voters_status()
        return self
