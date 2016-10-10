
import collections
import json
import datetime
import logging

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django import template
from django.utils import formats

from utils.django.datetime_utils import convert_date_to_django_date_format

from ..utils import pretty_label_or_short_description, convert_boolean_to_bootstrap_icon


logger = logging.getLogger('django.development')


register = template.Library()


@register.inclusion_tag('admin/admin/_/display_bootstrap_fileinput.html')
def as_bootstrap_fileinput(form_filefield):

    filefield_display_html = form_filefield.as_widget(attrs={'style': 'display: none;'})

    return {
        'file': form_filefield,
        'filefield_display_html': filefield_display_html,
    }


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
def urlencode_with_considering_pagination(context, page, position):

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


@register.inclusion_tag('admin/admin/_/display_object_list.html')
def display_object_list(model_admin, page_object_list):
    """

    """

    try:

        values_list = list()

        default_styles = {
            'align': 'left',
        }

        object_list = page_object_list.object_list
        fieldnames = [field.name for field in model_admin.model._meta.get_fields()]

        columns_with_styles = {}

        styles_by_column = {
            column: styles
            for columns, styles in model_admin.get_list_display_styles()
            for column in columns
        }

        global_styles = styles_by_column.pop('__all__') if '__all__' in styles_by_column else dict()

        list_display_dict = dict.fromkeys(model_admin.get_list_display(), {})

        for column, styles in list_display_dict.items():

            value = default_styles.copy()
            value.update(global_styles)
            value.update(styles_by_column.get(column, {}))
            columns_with_styles[column] = value

        columns_with_styles = [
            (column_name, columns_with_styles[column_name])
            for column_name in model_admin.list_display
        ]

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

            for i, column_with_styles in enumerate(columns_with_styles):

                column_name, styles = column_with_styles

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
                class_align = styles['align']

                # keep value with styles as one cell of a row
                values.append((value, class_align))

            # keep all rows of a table
            values_list.append((row_color, obj.pk, values))

        return {
            'values_list': values_list,
        }

    except Exception as e:
        logger.error('Tag does not working: %s' % e)


@register.inclusion_tag('admin/admin/_/display_date_hierarchy.html', takes_context=True)
def display_date_hierarchy(context, model_admin, object_list):
    """

    """

    if model_admin.date_hierarchy:

        try:

            request = context['request']

            field_name = model_admin.date_hierarchy

            field = model_admin.model._meta.get_field(field_name)
            method_dates_datetimes = 'datetimes' if isinstance(field, models.DateField) else 'dates'

            # variables for look up values in querystring
            field_name__year = field_name + '__year'
            field_name__month = field_name + '__month'
            field_name__day = field_name + '__day'

            # get values from querystring needed to build hierarchy of dates
            GET_ = request.GET.copy()
            year_lookup = GET_.pop(field_name__year, None)
            month_lookup = GET_.pop(field_name__month, None)
            day_lookup = GET_.pop(field_name__day, None)

            # again fetch values from queryset, because after paginatation
            # do not possible get results .dates() or .datetimes() from object_list
            object_list = object_list.model._default_manager.filter(pk__in=object_list.values('pk'))

            # if date_hierarchy is not used early
            # build date_hierarchy by years - from min to max
            if not year_lookup and not month_lookup and not day_lookup:

                max_min_dates = object_list.aggregate(
                    min_date=models.Min(field_name),
                    max_date=models.Max(field_name),
                )
                min_dates, max_dates = max_min_dates['min_date'], max_min_dates['max_date']

                # get all dates by years or if it one use it
                if min_dates.year != max_dates.year:
                    dates_datetimes = getattr(object_list, method_dates_datetimes)(field_name, 'year')
                else:
                    dates_datetimes = [min_dates]

                # build hierarchy by years
                choices = []
                for date_datetime in dates_datetimes:

                    # make GET querystring with respect old values and a year
                    year = date_datetime.year
                    GET_ = request.GET.copy()
                    GET_.__setitem__(field_name__year, year)
                    query_string = '?' + GET_.urlencode()

                    choices.append({
                        'link': query_string,
                        'display_text': year,
                    })

                # it opinion does not has path to back, so it will be not display
                back = {}

            # if hierarchy already built by a year, a month and a day
            if year_lookup and month_lookup and day_lookup:
                year_lookup = year_lookup[0]
                month_lookup = month_lookup[0]
                day_lookup = day_lookup[0]

                # create a mocked datetime object on based querystring
                selected_date = datetime.date(
                    year=int(year_lookup),
                    month=int(month_lookup),
                    day=int(day_lookup)
                )

                # use the mocked datetime object for make display_text as readonly (without link)
                choices = (
                    {
                        'link': None,
                        'display_text': formats.date_format(selected_date, 'MONTH_DAY_FORMAT'),
                    },
                )

                # make querystring for back link display as "Year, Month"
                GET_ = request.GET.copy()
                GET_.pop(field_name__day)
                query_string = '?' + GET_.urlencode()

                back = {
                    'query_string': query_string,
                    'display_text': formats.date_format(selected_date, 'YEAR_MONTH_FORMAT'),
                }

            # if hierarchy already built by a year and a month
            elif year_lookup and month_lookup:
                year_lookup = year_lookup[0]
                month_lookup = month_lookup[0]

                # all distinct dates/datetimes by day
                # keep as number of month and will be display as "Month, day"
                dates_datetimes = getattr(object_list, method_dates_datetimes)(field_name, 'day')
                dates_datetimes = (
                    {
                        'value': month,
                        'display_text': formats.date_format(month, 'MONTH_DAY_FORMAT'),
                    }
                    for month in dates_datetimes
                )

                # build hierarchy by days with corresponding querystring
                choices = []
                for date_datetime in dates_datetimes:

                    display_text = date_datetime['display_text']

                    value = date_datetime['value']
                    value = value.day

                    display_text = date_datetime['display_text']

                    GET_ = request.GET.copy()
                    GET_.__setitem__(field_name__year, year_lookup)
                    GET_.__setitem__(field_name__month, month_lookup)
                    GET_.__setitem__(field_name__day, value)
                    query_string = '?' + GET_.urlencode()

                    choices.append({
                        'link': query_string,
                        'display_text': display_text,
                    })

                # display back link as "Year, month" with corresponding querystring
                GET_ = request.GET.copy()
                GET_.pop(field_name__month)
                query_string = '?' + GET_.urlencode()

                # mocked datetime object
                date_ = datetime.date(
                    year=int(year_lookup), month=int(month_lookup), day=1,
                )
                back = {
                    'query_string': query_string,
                    'display_text': formats.date_format(date_, 'YEAR_MONTH_FORMAT'),
                }

            # if hierarchy already built by a year
            elif year_lookup:
                year_lookup = year_lookup[0]

                # all distinct dates/datetimes by month
                # keep as number of month and will be display as "Year, month"
                dates_datetimes = getattr(object_list, method_dates_datetimes)(field_name, 'month')
                dates_datetimes = (
                    {
                        'value': month,
                        'display_text': formats.date_format(month, 'YEAR_MONTH_FORMAT'),
                    }
                    for month in dates_datetimes
                )

                # build hierarchy by days with corresponding querystring
                choices = []
                for date_datetime in dates_datetimes:

                    display_text = date_datetime['display_text']

                    value = date_datetime['value']
                    value = value.month

                    display_text = date_datetime['display_text']

                    GET_ = request.GET.copy()
                    GET_.__setitem__(field_name__year, year_lookup)
                    GET_.__setitem__(field_name__month, value)
                    query_string = '?' + GET_.urlencode()

                    choices.append({
                        'link': query_string,
                        'display_text': display_text,
                    })

                # display back link as "Year, month" with corresponding querystring
                GET_ = request.GET.copy()
                GET_.pop(field_name__year)
                query_string = '?' + GET_.urlencode()
                back = {
                    'query_string': query_string,
                    'display_text': year_lookup,
                }

            return {
                'back': back,
                'choices': choices,
            }

        except Exception as e:
            logger.error('Tag does not working: %s' % e)


@register.inclusion_tag('admin/admin/_/display_table_header.html', takes_context=True)
def display_table_header(context, model_admin):

    ordering = context['ordering']

    model_meta = model_admin.model._meta

    concrete_fields = [field.name for field in model_meta.concrete_fields]

    applyed_ordering = dict()
    for position in range(len(ordering)):

        column = ordering[position]

        if column.startswith('-'):
            order = 'desc'
            column = column[1:]
        else:
            order = 'asc'

        position += 1

        applyed_ordering[column] = {
            'position': position,
            'order': order,
        }

    headers = list()
    for column_name in model_admin.list_display:

        # determination of display name of a column
        if hasattr(model_admin.model, column_name):
            attr = getattr(model_admin.model, column_name)
        elif hasattr(model_admin, column_name):
            attr = getattr(model_admin, column_name)

        if callable(attr):
            display_name = pretty_label_or_short_description(attr)
        elif isinstance(attr, property):
            attr = attr.fget
            display_name = pretty_label_or_short_description(attr)
        else:
            field = model_meta.get_field(column_name)
            display_name = field.verbose_name

        # determination is sortable column
        if column_name in concrete_fields:
            is_sortable = True
            is_method = False
        else:
            if getattr(model_admin.model, column_name, None):
                method = getattr(model_admin.model, column_name)
                is_sortable = True
            elif getattr(model_admin, column_name, None):
                method = getattr(model_admin, column_name)
                is_sortable = True
            else:
                is_sortable = False

            admin_order_field = method.admin_order_field
            is_method = True

        if is_method and admin_order_field in applyed_ordering.keys():
            current_applyed_ordering = applyed_ordering[admin_order_field]
            position = current_applyed_ordering['position']
            order = current_applyed_ordering['order']
        elif column_name in applyed_ordering.keys():
            current_applyed_ordering = applyed_ordering[column_name]
            position = current_applyed_ordering['position']
            order = current_applyed_ordering['order']
        else:
            position = None
            order = None

        sortable_data = json.dumps({
            column_name: {
                'position': position,
                'order': order,
            }
        })

        headers.append(
            {
                'sortable_data': sortable_data,
                'display_name': display_name,
                'is_sortable': is_sortable,
                'position': position,
                'order': order,
            }
        )

    return {
        'headers': headers,
    }


@register.inclusion_tag('admin/admin/_/display_fields.html')
def display_fields(model_meta):

    data = [
        (field.name, field.verbose_name, str(type(field)), field.help_text)
        for field in model_meta.concrete_fields
    ]

    return {
        'data': data
    }


@register.simple_tag(takes_context=True)
def display_admin_filter(context, filter_):

    request = context['request']
    template_ = template.loader.get_template(filter_.template)

    return template_.render(context=template.Context({
        'filter_': filter_,
        'details': filter_.get_details(request),
    }))
