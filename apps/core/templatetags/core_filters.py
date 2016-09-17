
from django import template


register = template.Library()


@register.filter
def has_registered_app_admin(app_label):

    return False
    return app_label
