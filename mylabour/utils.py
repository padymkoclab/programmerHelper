
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

from django.template import Template, Context
# from django.utils import timezone
from django.db import models
from django.core.exceptions import ImproperlyConfigured

import factory
from pygments import lexers


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


def get_random_objects(queryset, count=1):
    """Return certain count random objects from queryset.
    If 'count' is great than queryset, then return all avaibled objects.
    If queryset is empty - raise error."""

    # preluminary restrictions
    assert isinstance(queryset, models.QuerySet) is True, 'Passed queryset is not subclass models.QuerySet'
    assert count > 0, 'Count random objects must be more 0'

    #
    if not queryset.count():
        raise queryset.model.DoesNotExist('Passed queryset is empty.')

    #
    if queryset.count() == 1:
        warnings.warn('In queryset only 1 object, thus returned it.', Warning)
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


def get_different_between_elements(sequence, left_to_right=True):
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


def show_concecutive_certain_element(sequence, element):
    iteration = iter(sequence)
    k = list()
    t = list()
    for i in iteration:
        if i == 1:
            t.append(i)
        else:
            if t:
                k.append(t)
            t = list()
    if t:
        k.append(t)
    return k


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
        raise ValueError("Words may can generated only on English or Russian ('en' or 'ru'). Set 'locale' to 'ru' or 'en'.")

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


def create_log_for_terminal(name='DefaultLog'):
    """Configure log for using in terminal."""

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(console)
    return logger


def configured_logging():
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to console
    console.setFormatter(formatter)
    # add console to logger
    logger.addHandler(console)
    return logger


if __name__ == "__main__":
    import doctest
    doctest.testmod()
