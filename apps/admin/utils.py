
from django.utils.text import capfirst


def pretty_label_or_short_description(function):

    if hasattr(function, 'short_description'):
        return function.short_description
    else:
        label = function.__name__
        label = label.replace('_', ' ')
        label = capfirst(label)
        return label
