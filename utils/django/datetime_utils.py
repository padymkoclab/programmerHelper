
import math
import datetime
import random

from django.utils import timezone
from django.template import Template, Context

# import ephem


def get_current_timezone_offset():
    """ """

    # datetime in UTC
    now = timezone.now()

    # localtime in current timezone
    tz = timezone.get_current_timezone()
    now = now.astimezone(tz=tz)

    # name of timezone
    tz_name = now.strftime('%Z')

    # improved displaing time of offset
    time_offset = now.strftime('%z')
    time_offset = '{sign} {hours}:{minutes}'.format(
        sign=time_offset[0],
        hours=int(time_offset[1:3]),
        minutes=time_offset[3:]
    )

    # return time of offset and name of timezone
    return '{0} {1}'.format(time_offset, tz_name)


def get_year_by_slavic_aryan_calendar(now):
    """Get year by Slavic-Aryan calendar on today.

    New year (Новолетие) by Slavic-Aryan Clandar starting in the day autum equinox.
    If the day autum equinox was passed of the current year,
    then from current year must be add 5509 years,
    else - 5508.

    Returns:
        [type] -- [description]
    """

    format_datetime = '%Y/%m/%d %H:%M:%S'
    str_datetime_next_autumn_equinox = str(ephem.next_autumn_equinox(now))
    datetime_next_autumn_equinox = timezone.datetime.strptime(str_datetime_next_autumn_equinox, format_datetime)

    # set timezone`s
    datetime_next_autumn_equinox = datetime_next_autumn_equinox.replace(tzinfo=now.tzinfo)

    if datetime_next_autumn_equinox.year > now.year:
        return now.year + 5509
    return now.year + 5508


def get_random_date_from_days_ago_to_now(start_date=None):
    """ """

    days_close_half_year_ago = 550
    now = timezone.now()

    if start_date is None:
        start_date = timezone.now() - timezone.timedelta(days=days_close_half_year_ago)

    diff_days = (now - start_date).days

    days_ago = random.randint(1, diff_days)

    date = now - timezone.timedelta(days=days_ago)

    return date


def convert_date_to_django_date_format(date):
    """ """

    if isinstance(date, datetime.datetime):
        django_format = "DATETIME_FORMAT"
    elif isinstance(date, datetime.date):
        django_format = "DATE_FORMAT"
    else:
        raise ValueError('Attribute "date" must be a instance of datetime.datetime or datetime.date')
    t = Template('{{ date_datetime|date:"%s" }}' % django_format)
    c = Context({'date_datetime': date})
    return t.render(c)


def get_number_week_in_month(datetime):
    """
    Return the week`s number in the current month.

    >>> 1 + 3
    2
    """

    # a number of the current day
    now_day = datetime.day

    # a date/datetime for begin the month
    begin_month = datetime.replace(day=1)

    # a day`s number of the month with respect a day`s number of start the month
    number_day_month_with_respect_day_start_month = begin_month.weekday() + now_day

    # make division on a count days in a week - 7, to ceil this value and tp return it
    number_week = math.ceil(number_day_month_with_respect_day_start_month / 7)
    return number_week
