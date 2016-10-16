
import logging
import socket
import urllib
import pprint
import pip
import pathlib
import time

from django import template
from django.utils import timezone
from django.db import connection

import factory
from pygments import lexers


__all__ = []


def get_output_from_DTL(string, context=None):

    context = {} if context is None else context

    if not isinstance(context, dict):
        raise TypeError('Context must be a Python dict')

    template_ = template.Template(string)
    output = template_.render(context=template.Context(context))
    return output


def display_last_sql_queries(count=1):
    """ """

    queries = connection.queries[-count:]
    print('\n-------------------------\n'.join(query['sql'] for query in queries))


def join_enumarate(sep, iterable) -> str:
    """ """

    iterable = ('{0}. {1}'.format(i + 1, str(obj)) for i, obj in enumerate(iterable))
    return sep.join(iterable)


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

    logger = logging('django.development')

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


def show_all_possible_fakers():

    all_formatters = list()
    for attribute in dir(factory.Faker._get_faker()):
        try:
            flag = False
            if not attribute.startswith('_'):
                flag = True
                factory.Faker(attribute).generate([])
        except:
            pass
        else:
            if flag:
                all_formatters.append(attribute)

    line = '-' * 80
    for formatter in all_formatters:
        print(line)
        print('factory.Faker({0})'.format(formatter))
        print(line)
        for i in range(10):
            output = factory.Faker(formatter).generate([])
            output = str(output)[:100]
            print('\t{0}'.format(output))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
