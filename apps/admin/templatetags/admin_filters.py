
from django import template

register = template.Library()


@register.filter
def get_item_by_key(dictionary, key):
    try:
        return dictionary[key]
    except:
        return ''
