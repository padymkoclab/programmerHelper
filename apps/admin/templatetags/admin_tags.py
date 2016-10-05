
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


@register.simple_tag(takes_context=True)
def urlencode_with_conssidering_pagination(context, page, position):

    try:

        if position == 'previous':
            num = page.previous_page_number()
        elif position == 'next':
            num = page.next_page_number()
        else:
            num = position

        if not isinstance(position, int) and num < 1:
            raise Exception('Invalid number page')

        request = context.get('request')

        querydict = request.GET.copy()

        querydict.pop('page', 1)

        list_per_page = request.resolver_match.func.view_initkwargs['model_admin'].list_per_page

        list_per_page = querydict.pop('list_per_page', [list_per_page])[-1]

        num = str(num)

        querydict.setdefault('page', num)
        querydict.setdefault('list_per_page', list_per_page)

        return '?' + querydict.urlencode()

    except ZeroDivisionError:
        return ''


@register.simple_tag
def get_addons_for_field(fieldline_field):

    field_name = fieldline_field.field.name

    form_addons = getattr(fieldline_field.field.form, 'addons', {})

    field_addons = form_addons.get(field_name)

    if field_addons is not None:
        return {
            'left': field_addons.get('left', None),
            'right': field_addons.get('right', None),
        }

    return
