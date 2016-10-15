
import warnings
import pdb
import random
import itertools
import re

from django.utils import timezone
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='up_down_chars')
def UpDownChars(value):
    """
    Format text where one letter in uppercase, but next - lowercase, and so on.
    """
    even_chars = value[0::2].upper()
    odd_chars = value[1::2].lower()
    sequence = itertools.zip_longest(odd_chars, even_chars, fillvalue='')
    return ''.join(map(lambda el: el[1] + el[0], sequence))


@register.filter(name='formatting_big_number')
def FormattingBigNumber(value, paraments=' &3'):
    """
    Format number in human-readeably view
    """
    separator, count_digits_in_block = paraments.split('&')
    count_digits_in_block = 3 if not count_digits_in_block else int(count_digits_in_block)
    rounded_number = round(value, 2)
    number = str(rounded_number)
    unit_number, *float_number = number.rsplit('.')
    count_unit_times_block_in_number, remainder = divmod(len(unit_number), count_digits_in_block)
    temp_list = list()
    starting_digits = unit_number[:remainder]
    unit_number = unit_number[remainder:]
    for i in range(0, count_unit_times_block_in_number):
        start = count_digits_in_block * i
        end = count_digits_in_block * (i + 1)
        temp_list.append(unit_number[start:end])
    result = starting_digits + separator + separator.join(temp_list)
    result = (result).strip(separator)
    if float_number:
        result = result + '.' + float_number[0]
    return result


@register.filter(name="display_last_sorted_by_field")
def DisplayLastSortedByField(list_objects, field_name):
    if list_objects:
        if hasattr(list_objects[0], field_name):
            list_objects.sort(key=lambda i: getattr(i, field_name), reverse=True)
            return list_objects[:5]
        else:
            raise AttributeError('Object type of {0} has no atrribute "{1}"'.format(type(list_objects[0]), field_name))
    else:
        return []


@register.filter(name="display_random_elements")
def DisplayRandomElements(list_objects, count_random_element=5):
    if count_random_element > len(list_objects):
        count_random_element = len(list_objects)
    return random.sample(list_objects, count_random_element)


@register.filter(name="display_dictionaries_most_biggest_by_records")
def DisplayDictionariesMostBiggestByRecords(list_objects, fields_name):
    if list_objects:
        result = list()
        for obj in list_objects:
            for related_field in fields_name.split(','):
                if hasattr(obj, related_field):
                    result.append((obj, getattr(getattr(obj, related_field), 'count')()),)
        result.sort(key=lambda i: i[1], reverse=True)
        result = list(key for key, value in result)
        return result[:5]
    else:
        return []


@register.filter(name='highlight_founded_text')
def HighlightFoundedText(text_variable, phrase):
    def on_what_change(match):
        return "<span class='highlight_founded_text'>{0}</span>".format(match.group(0))
    result = re.sub(phrase, on_what_change, text_variable, flags=re.I)
    return mark_safe(result)


@register.filter(name='count_time_existence')
def CountTimeExistence(datetime_object):
    now = timezone.now()
    if datetime_object > now:
        raise ValueError('Datetime object not must be in future')
    timedelta = now - datetime_object
    result = timedelta.days + 1
    return result


@register.filter(name='display_sing_number')
def DisplaySingNumber(number):
    if number == 0:
        return number
    else:
        return '{0:+}'.format(number)


@register.filter(name='ipdb')
def ipdb(i):
    try:
        import ipdb
        ipdb.set_trace()
    except ImportError:
        warnings.warn('Module "ipdb" not found, then will be use module "pdb"', ImportWarning)
        pdb.set_trace()
    return i


@register.filter(name='has_admin_url')
def has_admin_url(model_admin, url_name):
    """ """
    return any(url for url in model_admin.urls if str(url.name).endswith('_{0}'.format(url_name)))
