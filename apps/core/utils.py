
from django.utils import timezone

import pygal
from dateutil.relativedelta import relativedelta

from apps.notifications.constants import Actions
from apps.notifications.models import Notification


def get_statistics_count_objects_for_the_past_year(queryset, date_field_name):
    """ """

    now = timezone.now()

    # get datetime on eleven months ago
    # owing to a number of month will be unique
    eleven_months_ago = now - relativedelta(months=11)

    # set in first day of month
    eleven_months_ago = eleven_months_ago.replace(day=1)

    # filter votes for a last 11 months and current month
    filter_lookup = '%s__gte' % date_field_name
    conditions_filter = {filter_lookup: eleven_months_ago}
    votes = queryset.filter(**conditions_filter)

    number_current_month = now.month
    number_current_year = now.year

    numbers_all_months = list(range(1, 13))

    # make reorder for order all numbers of months
    # where a number of current month is last, whereas a following month is first
    numbers_all_months = numbers_all_months[number_current_month:] + numbers_all_months[:number_current_month]

    #
    result = list()
    for number_month in numbers_all_months:

        # if is number month is more than current, that in month of past year
        year = number_current_year
        if number_month > number_current_month:
            year = number_current_year - 1

        # get abbr local name of month and year
        date_label = now.replace(year=year, month=number_month, day=1).strftime('%b %Y')

        # filter objects for that number of month
        filter_lookup = '%s__month' % date_field_name
        conditions_filter = {filter_lookup: number_month}
        count_obj_in_that_month = votes.filter(**conditions_filter).count()

        #
        result.append((date_label, count_obj_in_that_month))

    return result


def get_chart_count_objects_for_the_past_year(statistics_data):
    """ """

    config = pygal.Config(
        fill=True,
        show_legend=False,
        x_label_rotation=-45,
    )

    chart = pygal.StackedLine(config)

    dates, data = zip(*statistics_data)

    chart.x_labels = dates
    chart.add('Count objects', data)
    svg = chart.render()
    return svg


def get_user_reputation_by_notifications(user):
    """
    Getting reputation of user for activity on website:
    marks of published snippets, answers, questions and rating of articles,
    participate in polls.
    ---------------------------------------
        Evaluate reputation for activity
    ---------------------------------------
    Mark answers                   +3
    Mark questions                 +2
    Mark solutions                 +2
    Mark articles                +mark
    Mark snippets                  +2
    Participate in poll            +1

    +1 for each 1000 views
        Topic
        Article
        Question
        Solution
        Snippet

    ---------------------------------------
    """

    notifications = Notification.objects.filter(recipient=user)

    reputation = 0

    count_participate_in_poll = notifications.filter(action=Actions.PARTICIPATE_IN_POLL.value).count()
    count_undo_participate_in_poll = notifications.filter(action=Actions.UNDO_PARTICIPATE_IN_POLL.value).count()

    reputation += count_participate_in_poll
    reputation -= count_undo_participate_in_poll

    # count_upvote = notifications.filter(action=Actions.UPVOTE.value).count()
    # count_downvote = notifications.filter(action=Actions.DOWNVOTE.value).count()
    # count_lose_upvote = notifications.filter(action=Actions.LOSE_UPVOTE.value).count()
    # count_lose_downvote = notifications.filter(action=Actions.LOSE_DOWNVOTE.value).count()
    # count_change_to_upvote = notifications.filter(action=Actions.CHANGE_TO_UPVOTE.value).count()
    # count_downvote = notifications.filter(action=Actions.DOWNVOTE.value).count()
    # count_change_to_downvote = notifications.filter(action=Actions.CHANGE_TO_DOWNVOTE.value).count()

    return reputation
