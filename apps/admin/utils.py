
from importlib import import_module

from django.apps import apps
from django.utils.text import capfirst
from django.utils.html import format_html


def pretty_label_or_short_description(function):

    if hasattr(function, 'short_description'):
        return function.short_description
    else:
        label = function.__name__
        label = label.replace('_', ' ')
        label = capfirst(label)
        return label


def get_field_verbose_name_from_lookup(lookup, model):

    initial_model = model

    lookups = lookup.split('__')

    for i, lookup in enumerate(lookups):
        field = model._meta.get_field(lookup)

        if not i == len(lookups) - 1:
            model = field.related_model

    if initial_model != model:
        return '{} ({})'.format(field.verbose_name, model._meta.verbose_name)
    return field.verbose_name


def convert_boolean_to_bootstrap_icon(value):

    if value is True:
        bootstap_class = 'ok-sign'
        color = 'rgb(0, 255, 0)'
    elif value is False:
        bootstap_class = 'remove-sign'
        color = 'rgb(255, 0, 0)'
    elif value is None:
        bootstap_class = 'question-sign'
        color = 'rgb(0, 0, 0)'

    return format_html(
        '<span class="glyphicon glyphicon-{}" style="color: {}"></span>',
        bootstap_class, color
    )


def autodiscover_modules(filename):
    for app_config in apps.app_configs.values():
        try:
            import_module('{}.{}'.format(app_config.name, filename))
        except ImportError:
            pass
