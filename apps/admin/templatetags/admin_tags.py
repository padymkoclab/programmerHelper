
import logging

from django.utils.html import mark_safe
from django import template


logger = logging.getLogger('django.development')


register = template.Library()


@register.simple_tag(takes_context=True)
def prepopulated_fields_js(context):

    try:
        model_admin = context['model_admin']
        form = context['form']
        prepopulated_fields = model_admin.prepopulated_fields

        if prepopulated_fields == {}:
            return ''

        js_scripts = list()

        for field_name, field_names in prepopulated_fields.items():

            field_id = ['#' + field.id_for_label for field in form.form if field.name == field_name][0]

            field_ids = [
                '#' + field.id_for_label
                for field in form.form
                if field.name in field_names
            ]

            field_ids = ','.join(field_ids)

            js_script = "<script>$('{}').prepopulated_field('{}');</script>".format(field_id, field_ids)

            js_scripts.append(js_script)

        js_scripts = ''.join(js_scripts)

        return mark_safe(js_scripts)

    except Exception as e:
        logger.critical('Does not working "prepopulated_fields": {}'.format(e))
        return ''
