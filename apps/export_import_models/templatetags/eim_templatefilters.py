
from django.utils.html import format_html, format_html_join, mark_safe
from django.template import Library


register = Library()


@register.filter
def convert_boolean_in_colored_html(boolean_value):
    """ """

    if boolean_value is True:
        color = 'rgb(0, 255, 0)'
    else:
        color = 'rgb(240, 0, 0)'
    return format_html('<span style="color: {0}">{1}</span>', color, boolean_value)


@register.filter
def covert_dict_errors_to_beaty_html(dict_errors):
    """ """

    if not dict_errors:
        return ''

    fields_errors = ''
    for fieldname, error_lst in dict_errors.message_dict.items():
        errors = format_html_join(', ', '{0}', ((error, ) for error in error_lst))
        field_errors = format_html('{0}: {1}<br />', fieldname, errors)
        fields_errors += field_errors
    return mark_safe(fields_errors)
