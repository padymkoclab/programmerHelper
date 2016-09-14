
from django.utils import timezone

import pygal
from dateutil.relativedelta import relativedelta


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

    config = pygal.Config()
    config.width = 800
    config.height = 500
    config.explicit_size = True
    config.fill = True
    config.show_legend = False

    chart = pygal.StackedLine(config)

    dates, data = zip(*statistics_data)

    chart.x_labels = dates
    chart.add('Count objects', data)
    svg = chart.render()
    return svg
