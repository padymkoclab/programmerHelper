
import logging

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
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


@register.inclusion_tag('admin/admin/_/display_object_list.html', takes_context=True)
def display_object_list(context):
    """

    """

    try:

        values_list = list()

        table_header = context['table_header']
        model_admin = context['model_admin']
        page_object_list = context['page_object_list']

        object_list = page_object_list.object_list
        fieldnames = [field.name for field in model_admin.model._meta.get_fields()]

        def convert_boolean_to_bootstrap_icon(value):

            if value is True:
                bootstap_class = 'ok-sign'
                color = 'rgb(0, 255, 0)'
            elif value is False:
                bootstap_class = 'remove-sign'
                color = 'rgb(255, 0, 0)'
            elif value is None:
                bootstap_class = 'question-sign'
                color = 'rgb(0, 0, 0)'

            return format_html(
                '<span class="glyphicon glyphicon-{}" style="color: {}"></span>',
                bootstap_class, color
            )

        for obj in object_list:

            # determination row color
            colored_rows_by = model_admin.get_colored_rows_by()
            row_color = None
            if hasattr(model_admin, colored_rows_by):
                colored_rows_by = getattr(model_admin, colored_rows_by)
                row_color = colored_rows_by(obj)

            # url to add/chage page of thi object
            change_url = model_admin.site_admin.get_url(
                'change', model_admin.model._meta, kwargs={'pk': obj.pk}
            )

            # keep all values with styles
            values = list()
            for i, info in enumerate(table_header.items()):

                column_name, options = info

                # try get value from method of the model admin class
                if hasattr(model_admin, column_name):
                    model_admin_method = getattr(model_admin, column_name)
                    value = model_admin_method(obj)

                # try get value from method or field of the model
                elif hasattr(obj, column_name):
                    value = getattr(obj, column_name)

                    # method of the model
                    if callable(value):

                        if hasattr(value, 'boolean'):
                            value = value()
                            value = convert_boolean_to_bootstrap_icon(value)
                        else:
                            value = value()

                    # field of the model
                    elif column_name in fieldnames:

                        field = model_admin.model._meta.get_field(column_name)

                        # field with attribute 'choices'
                        if field.choices:
                            value = getattr(obj, 'get_{}_display'.format(column_name))()

                        # logical field will be returned as corresponding icon
                        if isinstance(field, (models.NullBooleanField, models.BooleanField)):
                            value = convert_boolean_to_bootstrap_icon(value)

                # if values is not end it is not models.NullBooleanField
                if value is None:
                    value = model_admin.site_admin.empty_value_display

                # determinate fields with the link to the page add/change
                # by default it first field
                if model_admin.list_display_links:
                    if column_name in model_admin.list_display_links:
                        value = format_html('<a href="{}">{}</a>', change_url, value)
                else:
                    if i == 0:
                        value = format_html('<a href="{}">{}</a>', change_url, value)

                # styles for column
                styles = options['styles']
                class_align = styles['align']

                # keep value with styles as one cell of a row
                values.append((value, class_align))

            # keep all rows of a table
            values_list.append((row_color, obj.pk, values))

        return {
            'values_list': values_list,
        }

    except ZeroDivisionError as e:
        logger.error('Tag does not working: %s' % e)
