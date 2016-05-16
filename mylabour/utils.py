
import random
import json

from django.db import models
from django.core.exceptions import ImproperlyConfigured

from pygments import lexers


CHOICES_LEXERS = [
    ('Awk', 'Awk'),
    ('Base Makefile', 'Base Makefile'),
    ('Bash', 'Bash'),
    ('CoffeeScript', 'CoffeeScript'),
    ('CSS', 'CSS'),
    ('CSS+Django/Jinja', 'CSS+Django/Jinja'),
    ('CSS+PHP', 'CSS+PHP'),
    ('CSS+Ruby', 'CSS+Ruby'),
    ('Django/Jinja', 'Django/Jinja'),
    ('HTML', 'HTML'),
    ('HTML+Django/Jinja', 'HTML+Django/Jinja'),
    ('HTML+PHP', 'HTML+PHP'),
    ('IPython3', 'IPython3'),
    ('Java', 'Java'),
    ('JavaScript', 'JavaScript'),
    ('JavaScript+Django/Jinja', 'JavaScript+Django/Jinja'),
    ('JavaScript+PHP', 'JavaScript+PHP'),
    ('JavaScript+Ruby', 'JavaScript+Ruby'),
    ('JSON', 'JSON'),
    ('LessCss', 'LessCss'),
    ('Makefile', 'Makefile'),
    ('MySQL', 'MySQL'),
    ('NumPy', 'NumPy'),
    ('Perl', 'Perl'),
    ('Perl6', 'Perl6'),
    ('PHP', 'PHP'),
    ('PostgreSQL console (psql)', 'PostgreSQL console (psql)'),
    ('Python', 'Python'),
    ('Python 3', 'Python 3'),
    ('reStructuredText', 'reStructuredText'),
    ('Ruby', 'Ruby'),
    ('Sass', 'Sass'),
    ('Scala', 'Scala'),
    ('SCSS', 'SCSS'),
    ('SQL', 'SQL'),
    ('XML', 'XML'),
    ('YAML', 'YAML'),
]


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
        if count > count_primary_keys:
            count = count_primary_keys
        if count_primary_keys == 0:
            raise ValueError('QuerySet is empty.')
        random_pks = random.sample(all_primary_keys, count)
        random_objects = queryset.filter(pk__in=random_pks)
        return random_objects
    else:
        raise TypeError('Type queryset must be \'django.db.models.query\'.')
