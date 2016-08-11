
from django.utils.html import format_html
from django.template import Library


register = Library()


@register.filter
def convert_boolean_in_colored_html(value):
    if value is True:
        color = 'rgb(0, 255, 0)'
    else:
        color = 'rgb(240, 0, 0)'
    return format_html('<span style="color: {0}">{1}</span>', color, value)
