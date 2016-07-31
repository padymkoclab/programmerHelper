
import socket
import datetime
import math
import logging
import warnings
import urllib
import collections
import re
import string
import pprint
import pip
import pathlib
import time
import random
import json

from django.shortcuts import _get_queryset
from django.utils import timezone
from django.template import Template, Context
from django.db import models
from django.core.exceptions import ImproperlyConfigured

import factory
from dateutil.relativedelta import relativedelta
from pygments import lexers

import ephem


__all__ = []


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


def get_random_objects(queryset, count, single_as_qs=False):
    """Return certain count random objects from queryset.
    If 'count' is great than queryset, then return all avaibled objects.
    If queryset is empty - raise error."""

    # preluminary restrictions
    if not isinstance(queryset, models.QuerySet):
        raise ValueError('Passed queryset is not subclass models.QuerySet')

    #
    if count < 1:
        return queryset.none()

    #
    if not queryset.count():
        raise queryset.model.DoesNotExist('Passed queryset is empty.')

    #
    if queryset.count() == 1:
        warnings.warn('In queryset only 1 object, thus returned it.', Warning)
        if single_as_qs:
            return queryset.filter()
        return queryset.first()

    #
    all_primary_keys = list(queryset.values_list('pk', flat=True))
    if len(all_primary_keys) < count:
        raise ValueError('Deficiently objects for choice.')

    #
    random.shuffle(all_primary_keys)
    choiced_primary_keys = all_primary_keys[:count]
    random_objects = queryset.filter(pk__in=choiced_primary_keys)

    #
    if count == 1:
        if single_as_qs:
            return queryset.filter()
        return random_objects.first()

    # prevent dublicates through SQL
    random_objects = random_objects.distinct()

    return random_objects


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


def generate_text_by_min_length(min_length, as_p=False):
    """Generate random text by minumim length.
    If parameter 'as_p' is true, at that time text will be as HTML paragraph."""

    # validation input
    if not isinstance(min_length, int):
        raise TypeError('Min length text must positive integer, not {0}'.format(type(min_length)))
    if min_length < 1:
        raise ValueError('Min length text must positive integer, not {0}'.format(min_length))
    # initialization
    method = 'p' if as_p is True else ''
    text = str()
    counter_iterations = 1
    # populate text
    while min_length > len(text):
        pattern = '{% lorem ' + str(counter_iterations) + ' ' + method + ' random %}'
        block_text = Template(pattern).render(Context())
        text = '{0}\n\n{1}'.format(text, block_text).strip()
        counter_iterations += 1
    return text


def generate_text_certain_length(length, locale='en'):
    """Generate text certain length with full-featured sentences."""

    # generate random text
    text = generate_text_by_min_length(length)
    assert len(text) >= length
    if len(text) == length:
        return text
    # make text approximate certain length
    while len(text) < length:
        text = text + ' ' + factory.Faker('text', locale=locale).generate([])
    # made full-fetured ending text for last sentence
    if len(text) != length:
        # slice text to certain length
        text = text[:length]
        # find last next-to-last sentence, if is
        next_to_last_sentence = text.rfind('.', 0, -1)
        if next_to_last_sentence != -1:
            # made lower ending last sentence and remove next-to-last point
            ending = text[next_to_last_sentence:].lower()
            text = text[:next_to_last_sentence] + ending[1:]
        # replace last space (if is) on character
        if text[-1] == ' ':
            text = text[:-1] + random.choice(string.ascii_lowercase)
        # replace next-to-last space (if is) on character
        if text[-2] == ' ':
            text = text[:-2] + random.choice(string.ascii_lowercase) + text[-1]
        # replace last point (if is) on character
        if text[-1] == '.':
            text = text[:-1] + random.choice(string.ascii_lowercase)
    if len(text) == length:
        text = text[:-1]
    # set point in ending of sentence
    text += '.'
    return text


def findall_words(text):
    """
    Find and return words in text.

    >>> findall_words('')
    []
    >>> findall_words('text')
    ['text']
    >>> findall_words('No problem, provided that the traceback is the only output.')
    ['No', 'problem', 'provided', 'that', 'the', 'traceback', 'is', 'the', 'only', 'output']
    >>> findall_words('A number of option flags control various aspects of doctest’s behavior.')
    ['A', 'number', 'of', 'option', 'flags', 'control', 'various', 'aspects', 'of', 'doctest’s', 'behavior']
    """

    if not isinstance(text, str):
        raise TypeError('Must be passed string, not {0}'.format(type(text)))
    if text:
        # complile basic chars of punctuation for removing it from string
        basic_chars_punctuation = re.compile('[{0}]'.format('!"#$%&\()*+,/:;<=>?@[\\]^_`{|}~'))
        # clean basic chars of punctuation from text
        text = basic_chars_punctuation.sub(' ', text)
        # remove ending point (in sentence)
        text = re.sub(r' *\. *$', '', text)
        # remove point in endgin nested sentence, if it have
        # or remove point in sentence break as paragraph
        text = re.sub(r'(\. )|(\.\n)', ' ', text)
        # remove char ' on sides words
        text = re.sub(r'(\' )|( \')', ' ', text)
        # remove dash
        text = re.sub(r'\W-\W', ' ', text)
        # getting words by split string and return it
        words = text.split()
        return words
    return []


def count_words(text):
    """Return count words in text."""

    if not isinstance(text, str):
        raise TypeError('Must be passed string, not {0}'.format(type(text)))
    if text:
        words = findall_words(text)
        len(words)
    return 0


def counter_words(text, ignorecase=False):
    """Count words in text with register and without it."""

    if not isinstance(text, str):
        raise TypeError('Must be passed string, not {0}'.format(type(text)))
    if text:
        words = findall_words(text)
        if ignorecase is True:
            words = (word.lower() for word in words)
        return collections.Counter(words)
    return 0


def has_connect_to_internet():
    """Checkup connect to interner."""

    try:
        urllib.request.urlopen('https://www.google.com')
    except urllib.error.URLError:
        return False
    else:
        return True


def generate_words(min_count_words, max_count_words, to_register='capitalize', locale='en'):
    """
    Generate words separated commas by passed count min and max needed words.
    Returned words may be as capitalize, upper, lower or title of each.
    Word may can contains unicode or ascii letters and controling with parameter 'locale'.

    >>> words = generate_words(1, 3)
    >>> len(words) in [1, 2, 3]
    True
    >>> words = generate_words(60, 60)
    >>> len(words) == 60
    True
    """

    #
    # Validation of input
    #

    # limiters must be integer
    if not (isinstance(min_count_words, int) and isinstance(max_count_words, int)):
        raise ValueError('Values \'min_count_words\' and \'max_count_words\' must be integer.')

    # min limiter must not great max limiter
    if min_count_words > max_count_words:
        raise ValueError('Min limiter count of the words must be not great than max limiter count of a words.')

    # limiters must be more than 0
    if not (min_count_words > 0 and max_count_words > 0):
        raise ValueError('Values \'min_count_words\' and \'max_count_words\' must be 1 or more.')

    # validate values of parameter 'to_register'
    if to_register not in ['capitalize', 'lower', 'title', 'upper']:
        raise ValueError("Values register of words must be 'capitalize', 'lower', 'title' or 'upper'.")

    # validate values of parameter 'locale'
    if locale not in ['ru', 'en']:
        raise ValueError(
            "Words may can generated only on English or Russian ('en' or 'ru'). Set 'locale' to 'ru' or 'en'."
        )

    #
    # Generate words
    #

    # generate random text with regards locale and getting words more or equal max needed
    random_words = list()
    while len(random_words) < max_count_words:
        text = factory.Faker('text', locale=locale).generate(())
        detected_words = findall_words(text)
        random_words.extend(detected_words)

    # slice determined count random_words
    number_for_slice = random.randint(min_count_words, max_count_words)
    slices_random_words = random_words[:number_for_slice]

    # applying function 'to_register' for each word
    words = list()
    for i, word in enumerate(slices_random_words):
        word = eval('"{word}".{function}()'.format(word=word, function=to_register))
        if to_register == 'capitalize' and i > 0:
            word = word.lower()
        words.append(word)
    return words


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


def random_text(count_sentences=3):
    """
    Analogy familiar 'Lorem', but realized on the pure Python.

    >>> random_text = random_text()
    >>> len(random_text.split('.'))
    3
    >>> random_text = random_text(78)
    >>> len(random_text.split('.'))
    78
    >>> random_text = random_text(2)
    >>> len(random_text.split('.'))
    2
    >>> random_text = random_text(1)
    >>> lst = random_text.split('.')
    >>> len(lst)
    2
    >>> lst[1]
    ''
    >>> random_text.count('.')
    1
    >>> random_text = random_text(0)
    >>> len(random_text)
    0
    >>> random_text
    ''
    >>> random_text = random_text(-1)
    >>> len(random_text)
    0
    >>> random_text
    ''
    """

    # make triple an all ascii-lower letters,
    # for ability a choice one character not once in word
    TRIPLE_CHARS = string.ascii_lowercase * 3

    # a list all a generated sentences
    sentences = list()

    # generate sentences
    for i in range(count_sentences):

        # list an all words in a sentence
        sentence = list()

        # random count a words in the sentence
        count_words_in_sentence = random.randint(3, 30)

        # generate words
        for j in range(count_words_in_sentence):

            # random length of a word
            word_length = random.randint(1, 20)

            # generate word by length
            for k in range(word_length):

                # a list of a chars, used in the word
                list_chars_in_words = random.sample(TRIPLE_CHARS, word_length)

                # make the list of the chars to string
                word = ''.join(list_chars_in_words)

            # add the word to the sentence
            sentence.append(word)

        # make the sentence from list to string, where a words will be separated by the gap
        sentence = ' '.join(sentence)

        # the sentence must be begin from a word with a big first letter
        sentence = sentence.capitalize()

        # the sentence must be end at the point
        sentence = sentence + '.'

        # add the sentence to the list of sentences
        sentences.append(sentence)

    # make the list of sentences to string, where an each sentence will be separated by the gap
    sentences = ' '.join(sentences)

    # return random text
    return sentences


def get_year_by_slavic_aryan_calendar(self):
    """Get year by Slavic-Aryan calendar on today.

    New year (Новолетие) by Slavic-Aryan Clandar starting in the day autum equinox.
    If the day autum equinox was passed of the current year,
    then from current year must be add 5509 years,
    else - 5508.

    Returns:
        [type] -- [description]
    """

    now = timezone.now()

    format_datetime = '%Y/%m/%d %H:%M:%S'
    str_datetime_next_autumn_equinox = str(ephem.next_autumn_equinox(now))
    datetime_next_autumn_equinox = timezone.datetime.strptime(str_datetime_next_autumn_equinox, format_datetime)

    # set timezone`s
    datetime_next_autumn_equinox = datetime_next_autumn_equinox.replace(tzinfo=now.tzinfo)

    if datetime_next_autumn_equinox.year > now.year:
        return now.year + 5509
    return now.year + 5508


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


def get_ip_from_request(request):
    """Return IP-address from request."""

    request.META.get('HTTP_X_FORWARDED_FOR')
    ip = request.META['REMOTE_ADDR']
    return ip


def get_location_from_ip(ip):
    """ """

    from django.contrib.gis.geoip2 import GeoIP2
    g = GeoIP2()
    try:
        location_detail = g.city(ip)
    except:
        ip = '91.202.144.122'
        location_detail = g.city(ip)
    return location_detail


def get_ip_by_host(host):
    """ """

    return socket.gethostbyname(host)


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
