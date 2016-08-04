
import socket
import logging
import warnings
import urllib
import pprint
import pip
import pathlib
import time
import random
import json

from django.shortcuts import _get_queryset
from django.utils import timezone
from django.db import models
from django.core.exceptions import ImproperlyConfigured

from dateutil.relativedelta import relativedelta
from pygments import lexers


__all__ = []


def join_enumarate(sep, iterable) -> str:
    """ """

    iterable = ('{0}. {1}'.format(i + 1, str(obj)) for i, obj in enumerate(iterable))
    return sep.join(iterable)


def get_statistics_count_objects_by_year(model, date_field_name):
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
    votes = model.objects.filter(**conditions_filter)

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


def delete_or_create(model, field, value):
    pass


def get_secret_value_for_setting_from_file(setting_name, filename='secrets.json'):
    """Getting secrets settings for website from JSON-file."""
    try:
        with open(filename, 'r') as f:
            secrets_in_json = json.loads(f.read())
        return secrets_in_json[setting_name]
    except FileNotFoundError:
        raise FileNotFoundError('File "{0}" not found'.format(filename))
    except KeyError:
        message = 'Failed configured value for {0}'.format(setting_name.upper())
        raise ImproperlyConfigured(message)


def get_choice_lexers():
    """Method what return choises lexers for using in attribute choices in field of model."""

    # REQUIRED pygments

    all_lexers_names = list(lexer[0] for lexer in lexers.get_all_lexers())
    all_lexers_names.sort(key=lambda i: i.lower())
    CHOICES_LEXERS = list((lexer_name, lexer_name) for lexer_name in all_lexers_names)
    return CHOICES_LEXERS


def attempt_get_value_attribute_or_return_default(object, attribute, default):
    try:
        if not isinstance(attribute, str):
            attribute = str(attribute)
        value = getattr(object, attribute)
    except AttributeError:
        return default
    else:
        return value


def get_different_between_elements_in_sequence(sequence, left_to_right=True):
    """Return different between adjoining element in the one-nested sequence, with elements same types."""

    if hasattr(sequence, '__iter__'):
        lst = list()
        for i, el in enumerate(sequence):
            try:
                different = el - sequence[i + 1] if left_to_right else sequence[i + 1] - el
            except IndexError:
                pass
            else:
                lst.append(different)
        return lst
    raise TypeError('Type of sequence must iterable.')


def pip_installed_packages():
    """ """

    for package in pip.get_installed_distributions():
        date_installed_in_seconds = pathlib.os.path.getctime(package.location)
        date_installed = time.ctime(date_installed_in_seconds)
        msg = '{0:<30} {1:<10}'.format(date_installed, package.key)
        print(msg)


def get_paths_all_nested_files(path, show=False):
    """ """

    all_paths = list()
    tree = pathlib.os.walk(path)
    for root, dirs, files in tree:
        for d in dirs:
            all_paths.append('{0}/{1}'.format(root, d))
        for f in files:
            all_paths.append('{0}/{1}'.format(root, f))

    # distinct paths
    all_paths = set(all_paths)
    all_paths = list(all_paths)
    all_paths.sort()

    # show if required
    if show:
        pprint.pprint(all_paths, indent=8)
    return all_paths


def has_connect_to_internet():
    """Checkup connect to interner."""

    try:
        urllib.request.urlopen('https://www.google.com')
    except urllib.error.URLError:
        return False
    else:
        return True


def create_logger_by_filename(name):
    """Return a logger for with passed name."""

    # create log
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create handler for terminal
    terminalHandler = logging.StreamHandler()

    # set level messages for handler
    terminalHandler.setLevel(logging.DEBUG)

    # create formatter for handler
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter for handler
    terminalHandler.setFormatter(fmt)

    # add handler to logger
    logger.addHandler(terminalHandler)

    return logger


def get_filename_with_datetime(name, extension):
    """Return filename with determined name, current datetime in internation format and extension."""

    now = timezone.now()

    # truncated version datetime ISO format (withput microseconds and and timezone)
    datetime_ISO_format = now.strftime('%Y-%m-%d %H:%M:%S')

    return '{0} {1}.{2}'.format(name, datetime_ISO_format, extension)


def get_ip_from_request(request):
    """Return IP-address from request."""

    # request.META.get('HTTP_X_FORWARDED_FOR')
    ip = request.META['REMOTE_ADDR']
    return ip


def get_ip_by_host(host):
    """ """

    return socket.gethostbyname(host)


def get_location(request):
    """ """

    logger = create_logger_by_filename(__name__)

    # check up if is connect to internet
    if not has_connect_to_internet:
        logger.warn('Now you is offline, so not possible determinate your IP-address')
        return

    # get IP from request
    ip = get_ip_from_request(request)

    # check up if it is not localhost
    hostname = socket.gethostbyaddr(ip)[0]
    if hostname == 'localhost':
        logger.warn('Now you is on localhost, so not possible determinate your IP-address')
        return

    # create new Geo
    from django.contrib.gis.geoip2 import GeoIP2
    geo = GeoIP2()

    # determinate details about a location
    location = geo.city(ip)

    # return a name of city and a name of country from the determined location
    return '{city}, {country}'.format(
        city=location['city'],
        country=location['country_name'],
    )


def get_latest_or_none(model):
    """ """

    qs = _get_queryset(model)

    try:
        return qs.latest()
    except model.DoesNotExist:
        return


if __name__ == "__main__":
    import doctest
    doctest.testmod()
