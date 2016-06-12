
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
    """Getting certain count random objects from queryset and return as queryset.
    If 'count' is great than queryset, then return all avaibled objects.
    If queryset is empty - raise error."""
    # checkout type queryset
    if isinstance(queryset, models.QuerySet):
        all_primary_keys = tuple(queryset.values_list('pk', flat=True))
        count_primary_keys = len(all_primary_keys)
        if count_primary_keys == 0:
            raise ValueError('QuerySet is empty.')
        if count > count_primary_keys:
            count = count_primary_keys
        random_pks = random.sample(all_primary_keys, count)
        random_objects = queryset.filter(pk__in=random_pks)
        if count == 1:
            return random_objects.first()
        return random_objects
    else:
        raise TypeError('Type queryset must be \'django.db.models.query\'.')


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


def generate_text_certain_length(length):
    """Generate text certain length with full-featured sentences."""

    # generate random text
    text = factory.Faker('text').generate([])
    # make text approximate certain length
    while len(text) <= length:
        text = text + ' ' + factory.Faker('text').generate([])
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
        # set point in ending of sentence
        text += '.'
    return text


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


def findall_words(text):
    """

    Find and return words in text.
    >>> 1 + 1
    2
    >>>

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
    return 0


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


def genarete_words_separated_commas(count_words):
    """Generate words separated commas by passed count needed words."""

    raise NotImplementedError
