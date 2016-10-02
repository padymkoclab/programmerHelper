
import logging

from django.core.urlresolvers import reverse
from django import template

register = template.Library()
logger = logging.getLogger('django.development')


@register.filter
def get_item_by_key(dictionary, key):
    try:
        return dictionary[key]
    except:
        return ''


@register.filter
def add_classes_to_label_tag(field, classes):
    try:
        return field.label_tag(attrs={'class': classes})
    except:
        return ''


@register.filter
def get_admin_url(model_meta, url_main_name):
    try:
        if url_main_name == 'app':
            return reverse('admin:{}_index'.format(model_meta.app_label))
        elif url_main_name == 'add':
            return reverse('admin:{}_{}_add'.format(model_meta.app_label, model_meta.model_name))
        elif url_main_name == 'change':
            return reverse('admin:{}_{}_change'.format(model_meta.app_label, model_meta.model_name))
        elif url_main_name == 'delete':
            return reverse('admin:{}_{}_delete'.format(model_meta.app_label, model_meta.model_name))
        elif url_main_name == 'history':
            return reverse('admin:{}_{}_history'.format(model_meta.app_label, model_meta.model_name))
        elif url_main_name == 'changelist':
            return reverse('admin:{}_{}_changelist'.format(model_meta.app_label, model_meta.model_name))
    except Exception as e:
        logger.error('Does not working: {}'.format(e))
