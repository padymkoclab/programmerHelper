
import datetime
import itertools

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from utils.django.functions_db import Round

from apps.core.utils import (
    get_statistics_count_objects_for_the_past_year,
    get_chart_count_objects_for_the_past_year,
)


class PollsManager(models.Manager):
    """
    Manager for the user model.
    """

    def get_report_votes_of_user(self, user):
        """Return report about votes of a user as tuple of records.
        An each record is string contains information about vote, namely: choice and poll."""

        votes = user.votes.all()
        return tuple(
            _('Voted for a choice "{0}" in a poll "{1}"').format(vote.choice, vote.poll)
            for vote in votes
        )

    def get_count_votes_of_user(self, user):
        """Return a count votes """

        return user.votes.count()

    def get_votes_of_user(self, user):
        """Return all votes of a user."""

        return user.votes.all()

    def get_latest_vote_of_user(self, user):
        """Return latest vote of a user or None."""

        try:
            return user.votes.latest()
        except user.votes.model.DoesNotExist:
            return

    def is_active_voter(self, user):
        """Check up, a user is an active voter."""

        if user in self.get_most_active_voters():
            return True
        return False

    def get_all_voters(self):
        """Return all voters (users with at least 1 vote) in a descending order."""

        # annotate a count votes for an every user
        users_with_count_votes = self.users_with_count_votes()

        # filter users with votes
        all_voters = users_with_count_votes.filter(count_votes__gte=1)

        # order by users by count votes in a descending order
        return all_voters.order_by('-count_votes')

    def get_most_active_voters(self):
        """Return users, participated in more than a haft of polls in a descending order."""

        # determinate statuses of voters by activity in polls
        users_with_active_voters_status = self.model.polls.users_with_active_voters_status()

        # filter only active voters
        active_voters = users_with_active_voters_status.filter(is_active_voter=True)

        # return active voters in a descending order
        return active_voters.order_by('-count_votes')

    def _get_half_from_total_count_polls(self):
        """Return integer number, rounded to floor, corresponding to a half from total count polls."""

        # make an access to a related model
        related_model = self.model.votes.rel.related_model

        # total count polls
        count_polls = related_model.poll.get_queryset().count()

        # a half from count polls as integer
        return count_polls // 2


class PollManager(models.Manager):
    """
    Manager for polls
    """

    def get_avg_count_choices(self):
        """ """

        self = self.polls_with_count_choices()
        return self.aggregate(
            avg=Round(
                models.functions.Coalesce(
                    models.Avg('count_choices'),
                    0
                )
            )
        )['avg']

    def get_avg_count_votes(self):
        """ """

        self = self.polls_with_count_votes()
        return self.aggregate(
            avg=Round(
                models.functions.Coalesce(
                    models.Avg('count_votes'),
                    0
                )
            )
        )['avg']

    def get_count_opened_polls(self):
        """ """

        return self.filter(status=self.model.OPENED).count()

    def get_count_closed_polls(self):
        """ """

        return self.filter(status=self.model.CLOSED).count()

    def get_count_draft_polls(self):
        """ """

        return self.filter(status=self.model.DRAFT).count()

    def get_by_natural_key(self, title):
        return self.get(title=title)

    def change_status_poll(self, poll, status_name):
        """Change status of poll in place."""

        poll.status = status_name
        poll.full_clean()
        poll.save()

    def get_statistics_polls_by_status(self):
        """Return dictionary, where key is status`s name, value - number of polls with this status."""

        return {
            self.model.CHOICES_STATUS.opened: self.opened_polls().count(),
            self.model.CHOICES_STATUS.closed: self.closed_polls().count(),
            self.model.CHOICES_STATUS.draft: self.draft_polls().count(),
        }

    def get_average_count_votes_in_polls(self):
        """Return an average count votes on the polls."""

        polls_with_count_votes = self.polls_with_count_votes()
        avg_count_votes = polls_with_count_votes.aggregate(
            avg_count_votes=models.functions.Coalesce(
                Round(models.Avg('count_votes')), 0
            )
        )
        return avg_count_votes['avg_count_votes']

    def get_average_count_choices_in_polls(self):
        """Return an average count choices in the polls."""

        polls_with_count_choices = self.polls_with_count_choices()
        avg_count_choices = polls_with_count_choices.aggregate(
            avg_count_choices=models.functions.Coalesce(
                Round(models.Avg('count_choices')), 0
            )
        )
        return avg_count_choices['avg_count_choices']


class ChoiceManager(models.Manager):

    def get_avg_count_votes(self):
        """ """

        self = self.choices_with_count_votes()
        return self.aggregate(
            avg=Round(
                models.functions.Coalesce(
                    models.Avg('count_votes'),
                    0
                )
            )
        )['avg']


class VoteManager(models.Manager):
    """ """

    def get_count_distinct_voters(self):
        """ """

        return self.values('user').distinct().count()

    def get_statistics_count_votes_by_months_for_past_year(self):
        """Return a statistics of count votes in an each month for past year in next format
        [
            (eleven_months_ago, count_votes),
            (ten_months_ago, count_votes),
            (nine_months_ago, count_votes),
            (eight_months_ago, count_votes),
            (seven_months_ago, count_votes),
            (six_months_ago, count_votes),
            (five_months_ago, count_votes),
            (four_months_ago, count_votes),
            (three_months_ago, count_votes),
            (two_months_ago, count_votes),
            (one_month_ago, count_votes),
            (current_month, count_votes),
        ]

        month return as localized format - (month_name, year)
        """

        now = timezone.now()

        # date exactly eleven months ago
        exact_eleven_months_ago = now - relativedelta(months=11)

        # go to start new day of the first day a month
        eleven_months_ago = exact_eleven_months_ago.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # votes for this month and eleven months ago (considering from start day of first day month)
        objs = self.filter(date_voting__range=[eleven_months_ago, now])

        # iteration number months, starting in past year month + 1, ending in this month
        numbers_months = itertools.chain.from_iterable([range(now.month + 1, 12 + 1), range(1, now.month + 1)])

        result = []
        for month_number in numbers_months:
            # get an objects by the month`s number
            # given that, we have a dates range with an unique numbers of months
            objs_count = objs.filter(date_voting__month=month_number).count()

            # if number of month is more than current, than it was in past year
            if month_number > now.month:
                year = now.year - 1

            else:
                year = now.year

            # create a datetime object, in order to get string representation datetime as next: AbbrMonth, Year
            month_year_name = datetime.datetime(year=year, month=month_number, day=1).strftime('%b %Y')

            result.append((month_year_name, objs_count))

        return result

    def get_latest_vote(self):
        """ """

        try:
            return self.latest()
        except self.model.DoesNotExist:
            return

    def get_statistics_count_votes_for_the_past_year(self):
        """ """

        return get_statistics_count_objects_for_the_past_year(self, 'date_voting')

    def get_chart_count_votes_for_the_past_year(self):
        """ """

        return get_chart_count_objects_for_the_past_year(
            self.get_statistics_count_votes_for_the_past_year()
        )
