
import logging

from django.db import models
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
def get_admin_url(model_meta_or_object, url_main_name):
    try:

        if isinstance(model_meta_or_object, models.options.Options):

            model_meta = model_meta_or_object

            if url_main_name == 'app':
                return reverse('admin:{}_index'.format(model_meta.app_label))
            elif url_main_name == 'changelist':
                return reverse('admin:{}_{}_changelist'.format(model_meta.app_label, model_meta.model_name))
            elif url_main_name == 'add':
                return reverse('admin:{}_{}_add'.format(model_meta.app_label, model_meta.model_name))

        elif isinstance(model_meta_or_object, models.Model):

            object_ = model_meta_or_object

            if url_main_name == 'change':
                return reverse(
                    'admin:{}_{}_change'.format(object_._meta.app_label, object_._meta.model_name),
                    kwargs={'pk': object_.pk}
                )
            elif url_main_name == 'delete':
                return reverse(
                    'admin:{}_{}_delete'.format(object_._meta.app_label, object_._meta.model_name),
                    kwargs={'pk': object_.pk}
                )
            elif url_main_name == 'history':
                return reverse(
                    'admin:{}_{}_history'.format(object_._meta.app_label, object_._meta.model_name),
                    kwargs={'pk': object_.pk}
                )
        else:
            logger.error('Wrong input data')
    except Exception as e:
        logger.error('Does not working: {}'.format(e))


@register.filter
def show_all_objects(request, total_count_objects):

    var = 'list_per_page'

    GET_ = request.GET.copy()
    GET_.pop(var, None)
    GET_.setdefault(var, total_count_objects)

    return '?' + GET_.urlencode()
