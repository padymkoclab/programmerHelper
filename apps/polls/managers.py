
import datetime
import itertools

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta

# from apps.users.models import User


class PollManager(models.Manager):
    """
    Custom model manager for polls
    """

    def get_statistics_polls_by_status(self):
        """ """

        # return dictionary, where key is status`s display name, value - count that polls
        return {
            self.model.CHOICES_STATUS.opened: self.opened_polls().count(),
            self.model.CHOICES_STATUS.closed: self.closed_polls().count(),
            self.model.CHOICES_STATUS.draft: self.draft_polls().count(),
        }

    def most_active_voters(self):
        """A users participated in more than haft from all count polls."""

        User = get_user_model()
        half_count_polls = self.count() // 2
        users_with_count_votes = User.objects.users_with_count_votes()
        return users_with_count_votes.filter(count_votes__gt=half_count_polls)

    def get_all_voters(self):
        """ """

        User = get_user_model()
        users_with_count_votes = User.objects.users_with_count_votes()
        all_voters = users_with_count_votes.filter(count_votes__gt=0)
        all_voters = all_voters.order_by('-count_votes')
        return all_voters

    def get_count_voters(self):
        """ """

        return self.get_all_voters().count()

    def get_average_count_votes_in_polls(self):
        """Return an average count votes on the polls.

        [description]
        """

        polls_with_count_votes = self.polls_with_count_votes()
        avg_count_votes = polls_with_count_votes.aggregate(avg_count_votes=models.Avg('count_votes'))
        return avg_count_votes['avg_count_votes']

    def get_average_count_choices_in_polls(self):
        """Return an average count choices in the polls.

        [description]
        """

        polls_with_count_choices = self.polls_with_count_choices()
        avg_count_choices = polls_with_count_choices.aggregate(avg_count_choices=models.Avg('count_choices'))
        return avg_count_choices['avg_count_choices']


class VotesManager(models.Manager):
    """
    Custom model manager for votes
    """

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

        month return as localized format - month_name, year

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
