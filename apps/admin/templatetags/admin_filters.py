
import logging

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.urlresolvers import reverse
from django import template
from django.apps import AppConfig

from ..utils import convert_boolean_to_bootstrap_icon


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
def as_bootstrap_logic_icon(value):
    return convert_boolean_to_bootstrap_icon(value)


@register.filter
def get_admin_url(object_, url_main_name):

    try:

        if isinstance(object_, models.options.Options):

            model_meta = object_

            if url_main_name == 'app':
                return reverse('admin:{}_index'.format(model_meta.app_label))
            elif url_main_name == 'changelist':
                return reverse('admin:{}_{}_changelist'.format(model_meta.app_label, model_meta.model_name))
            elif url_main_name == 'add':
                return reverse('admin:{}_{}_add'.format(model_meta.app_label, model_meta.model_name))

        elif isinstance(object_, AppConfig):

            app_config = object_
            if url_main_name == 'app':
                return reverse('admin:{}_index'.format(app_config.label))

        elif isinstance(object_, models.Model):

            instance = object_

            if url_main_name == 'change':
                return reverse(
                    'admin:{}_{}_change'.format(instance._meta.app_label, instance._meta.model_name),
                    kwargs={'pk': instance.pk}
                )
            elif url_main_name == 'delete':
                return reverse(
                    'admin:{}_{}_delete'.format(instance._meta.app_label, instance._meta.model_name),
                    kwargs={'pk': instance.pk}
                )
            elif url_main_name == 'history':
                return reverse(
                    'admin:{}_{}_history'.format(instance._meta.app_label, instance._meta.model_name),
                    kwargs={'pk': instance.pk}
                )
            elif url_main_name == 'import':
                pk_model_content_type = ContentType.objects.get_for_model(instance).pk
                return reverse('admin:import_index')

        elif isinstance(object_, models.QuerySet):

            queryset = object_

            if url_main_name == 'export':
                pk_model_content_type = ContentType.objects.get_for_model(queryset.model).pk
                listing_pks_objects = ','.join(str(i['pk']) for i in queryset.only('pk').values('pk'))
                return reverse(
                    'admin:export_model',
                    kwargs={
                        'pk_model': pk_model_content_type,
                        'listing_pks_objects': listing_pks_objects,
                    }
                )
        else:
            raise Exception()
    except Exception as e:
        logger.error('Does not working: {}'.format(e))


@register.filter
def show_all_objects(request, total_count_objects):

    var = 'list_per_page'

    GET_ = request.GET.copy()
    GET_.pop(var, None)
    GET_.setdefault(var, total_count_objects)

    return '?' + GET_.urlencode()


@register.filter
def is_instance_exists(instance):
    return instance._meta.model._default_manager.filter(pk=instance.pk).exists()
