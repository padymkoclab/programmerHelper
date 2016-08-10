
import math
import textwrap
import datetime
from io import BytesIO
import warnings
import itertools
import csv
import collections
import uuid

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest, StreamingHttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, TemplateView, RedirectView
from django.core import serializers

import xlsxwriter

from config.admin import ProgrammerHelperAdminSite
from mylabour.utils import get_filename_with_datetime

from .forms import UploadSerializedFileForm


def made_validation(kwargs):

    # get model
    content_type_model_pk = int(kwargs['content_type_model_pk'])
    try:
        ct_model = ContentType.objects.get(pk=content_type_model_pk)
    except:
        return HttpResponseBadRequest(_('Not prossible get a data from the database. Corrupted input the data.'))
    model = ct_model.model_class()

    # get objects of model
    pks_separated_commas = kwargs['pks_separated_commas']
    list_pks_separated_commas = pks_separated_commas.split(',')
    try:
        qs = model.objects.filter(pk__in=list_pks_separated_commas)
        qs.count()
    except:
        return HttpResponseBadRequest(_('Not prossible get a data from the database. Corrupted input the data.'))

    # compare count got and requested the objects
    if len(list_pks_separated_commas) != len(qs):
        return HttpResponseBadRequest(_('A data were corrupted. Not all a primary key of the objects has in database.'))

    # get names of fields of model
    fields = kwargs['fields']
    list_fields = fields.split(',')
    # validation input field`s names
    for field in list_fields:
        try:
            model._meta.get_field(field)
        except FieldDoesNotExist:
            return HttpResponseBadRequest(_('Some field does not exist.'))

    return model, qs, list_fields


class ExportRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        app_label = kwargs.get('app_label', None)
        model_name = kwargs.get('model_name', None)
        pks_separated_commas = kwargs.get('pks_separated_commas', None)

        contenttype_model = get_object_or_404(ContentType, app_label=app_label, model=model_name)

        url = reverse(
            'export_import_models:export',
            kwargs={'content_type_model_pk': contenttype_model.pk, 'pks_separated_commas': pks_separated_commas}
        )

        return url


class ExportTemplateView(TemplateView):
    """
    View fo export
    """

    template_name = "export_import_models/admin/export.html"

    def get(self, request, *args, **kwargs):

        #
        content_type_model_pk = kwargs['content_type_model_pk']
        ct_model = ContentType.objects.get(pk=content_type_model_pk)
        model = ct_model.model_class()

        #
        pks_separated_commas = kwargs['pks_separated_commas']
        list_pks_separated_commas = pks_separated_commas.split(',')

        #
        try:
            count_objects = model.objects.filter(pk__in=list_pks_separated_commas).count()
        except ValueError:
            raise HttpResponseBadRequest(_('Not prossible get a data from the database. Corrupted input the data.'))

        #
        if len(list_pks_separated_commas) != count_objects:
            raise HttpResponseBadRequest(
                _('A data were corrupted. Not all a primary key of the objects has in database.'))

        # For only admin theme Django-Suit
        # It need namespace for display menu in left sidebar
        request.current_app = ProgrammerHelperAdminSite.name

        return super(ExportTemplateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExportTemplateView, self).get_context_data(**kwargs)

        #
        content_type_model_pk = kwargs['content_type_model_pk']
        ct_model = ContentType.objects.get(pk=content_type_model_pk)
        model = ct_model.model_class()
        model_verbose_name = model._meta.verbose_name
        app_verbose_name = model._meta.app_config.verbose_name

        #
        pks_separated_commas = kwargs['pks_separated_commas']
        list_pks_separated_commas = pks_separated_commas.split(',')
        queryset = model.objects.filter(pk__in=list_pks_separated_commas)

        #
        context['content_type_model_pk'] = content_type_model_pk
        context['fields'] = model._meta.fields
        context['queryset'] = queryset
        context['pks_separated_commas'] = pks_separated_commas
        context['django_admin_media'] = admin.ModelAdmin(get_user_model(), ProgrammerHelperAdminSite).media

        title = _('Export data from a model {0} (application {1})').format(model_verbose_name, app_verbose_name)
        context['title'] = title

        context.update(ProgrammerHelperAdminSite.each_context(self.request))

        return context


class ExportPreviewDownloadView(View):
    """

    """

    def get(self, request, *args, **kwargs):

        # data from hidden inputs
        pks_separated_commas = request.GET.get('pks_separated_commas')
        content_type_model_pk = request.GET.get('content_type_model_pk')

        # data from user
        format_export_data = request.GET.get('format_export_data')
        fields = request.GET.getlist('fields')

        allowed_formats_for_preview = ['json', 'yaml', 'xml']
        allowed_formats = allowed_formats_for_preview + ['csv', 'xlxs']

        if format_export_data not in allowed_formats:
            return HttpResponseBadRequest('Passed not supported format for export')

        if not (fields or format_export_data or pks_separated_commas or content_type_model_pk):
            return HttpResponseBadRequest('Something wrong with input')

        # get content_type_model by pk
        content_type_model = ContentType.objects.get(pk=content_type_model_pk)

        # get model of content_type_model
        model = content_type_model.model_class()

        # get list of primary keys of objects for export
        list_pks_separated_commas = pks_separated_commas.split(',')

        # get queryset of objects by their keys
        queryset = model.objects.filter(pk__in=list_pks_separated_commas)

        content_type = 'text/{0}'.format(format_export_data)
        response = HttpResponse(content_type=content_type)
        filename = 'filename.{0}'.format(format_export_data)

        if 'download' in request.GET:
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

            if format_export_data in allowed_formats_for_preview:

                # make serialization
                serializer = serializers.get_serializer(format_export_data)
                serializer = serializer()
                serializer.serialize(queryset, stream=response)

            else:
                if format_export_data == 'csv':
                    return HttpResponse('CSV')

            return response
        elif 'preview' in request.GET:
            if format_export_data not in allowed_formats_for_preview:
                return HttpResponseBadRequest('Preview accessibly only for JSON, XML, YAML.')

            # make serialization
            serializer = serializers.get_serializer(format_export_data)
            serializer = serializer()
            serializer.serialize(queryset, stream=response, fields=fields)

            return response
        return HttpResponseBadRequest('Not correct type of a request')

    def return_preview(self):
        pass


class ImportTemplateView(TemplateView):

    template_name = "export_import_models/admin/import.html"

    def dispatch(self, request, *args, **kwargs):

        # For only admin theme Django-Suit
        # It need namespace for display menu in left sidebar
        request.current_app = ProgrammerHelperAdminSite.name

        return super(ImportTemplateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        form = UploadSerializedFileForm()

        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = UploadSerializedFileForm(request.FILES)
        if form.is_valid():
            return HttpResponse('Hurrah!')

        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(ImportTemplateView, self).get_context_data(**kwargs)
        context['title'] = _('Import data in a model')

        return context


class ExportCSV(View):
    """
    View for export data of a models to CSV format
    """

    def _get_rows_as_generator(self, qs, list_fields):
        """Return a generator as a nested list, where each list is it a values need the fields."""

        for values_fields_of_obj in qs.values_list(*list_fields):
            # for each iteration return list values of the need fields
            yield values_fields_of_obj

    def generate_csv_as_stream(self, model, qs, list_fields, filename):
        """Generate the CSV file by help a stream and generator of the data.
        As result it is a very for high-production."""

        # get generator values for rows
        rows = self._get_rows_as_generator(qs, list_fields)

        # for properly adding list_fields in generator, make it two-nested list
        two_nested_list_fields = [list_fields]

        # concatenate list_fields with rows values
        rows = itertools.chain(two_nested_list_fields, rows)

        #
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        # write items generator in a stream adn attach file to it
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename

        return response

    def generate_csv_simple(self, model, qs, list_fields, filename):
        """Generate the CSV file straight way, make iteration on the objects and their fields."""

        # create response and attach to it file CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename

        # create a new writter and to write first row as the fields names
        writer = csv.writer(response)
        writer.writerow(list_fields)

        # write the values of fields as a row
        for values_fields_of_obj in qs.values_list(*list_fields):
            writer.writerow(values_fields_of_obj)

        return response

    def generate_csv_by_DTL(self, model, qs, list_fields, filename):
        """Generate the CSV using DTL."""

        # create response and attach file CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename

        # generate template that similar next
        # {% for row in data %}"{{ row.0|addslashes }}", "{{ row.1|addslashes }}", "{{ row.2|addslashes }}",
        # {% endfor %}
        start_loop_statement = "{% for row in data %}"
        end_loop_statement = "\n{% endfor %}"
        list_loop_rows = list()
        for i in range(len(list_fields)):
            loop_row = "\"{{ row.%d|addslashes }}\"" % i
            list_loop_rows.append(loop_row)
        loop_rows = ', '.join(list_loop_rows)

        # made natural Django Template from string
        template = Template(start_loop_statement + loop_rows + end_loop_statement)

        # add the names of fields as a first row and after rest a values fields of the objects
        data = [list_fields]
        data.extend(qs.values_list(*list_fields))

        # fill up context this newly created template
        context = Context({
            'data': data,
        })

        # write a values of fields from render the template with passed context
        response.write(template.render(context))

        return response

    def dispatch(self, request, *args, **kwargs):

        response = made_validation(kwargs)
        if isinstance(response, HttpResponseBadRequest):
            return response
        model, qs, list_fields = response
        filename = get_filename_with_datetime(name=model._meta.verbose_name_plural, extension='csv')

        warnings.warn('Choice good way', Warning)
        return self.generate_csv_by_DTL(model, qs, list_fields, filename)
        return self.generate_csv_as_stream(model, qs, list_fields, filename)
        return self.generate_csv_simple(model, qs, list_fields, filename)


class Echo(object):
    """
    An object that implements just the write method of the file-like interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class ExportExcel(View):
    """
    View for export data of a models to Excel
    """

    def dispatch(self, request, *args, **kwargs):
        raise NotImplementedError('Rewrite code on OpenPyXl')
        response = made_validation(kwargs)
        if isinstance(response, HttpResponseBadRequest):
            return response
        model, qs, list_fields = response
        filename = get_filename_with_datetime(name=model._meta.verbose_name_plural, extension='xlsx')

        return self.generate_excel_with_XlsxWriter(model, qs, list_fields, filename)

    def generate_excel_with_XlsxWriter(self, model, qs, list_fields, filename):
        """ """

        # dictionary for keeping all used count rows in each row
        dict_rows_rows = collections.defaultdict(set)
        # dictionary for keeping all used width column in each columns
        dict_columns_width = collections.defaultdict(set)

        response = HttpResponse(content_type='application/application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename

        #
        model_name = model._meta.verbose_name
        output = BytesIO()
        options = {
            'strings_to_formulas': True,
            'nan_inf_to_errors': True,
        }
        workbook = xlsxwriter.Workbook(output, options)

        # set properties of document
        workbook.set_properties({
            'title': _('Data from model "{0}"').format(model_name),
            'subject': '',
            'author': 'ProgrammerHelper.com',
            'manager': 'Dr. Heinz Doofenshmirtz',
            'company': 'of Wolves',
            'category': 'Example spreadsheets',
            'keywords': 'Data from model "{0}"'.format(model_name),
            'comments': 'Created with Python and XlsxWriter'
        })

        workbook.set_calc_mode('auto')

        # set custom properties
        # workbook.set_custom_property('Checked by', 'Admin')
        # workbook.set_custom_property('Date completed', 'Today')
        # workbook.set_custom_property('Document number', 1)
        # workbook.set_custom_property('Reference number', 1)
        # workbook.set_custom_property('Has review', 'No')

        #
        sheet1 = workbook.add_worksheet(_("Summary").format())

        # add formating
        format_total_count_objects = workbook.add_format({
            'border': 1,
            'color': '#ffff00',
            'bg_color': '#808080',
        })
        format_sign_numeration = workbook.add_format({
            'italic': True,
            'align': 'center',
            'border': 1,
        })
        format_field_name = workbook.add_format({
            'bold': True,
            'align': 'center',
            'border': 1
        })
        format_title = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
            'border': 6,
            'fg_color': '#D7E4BC',
        })
        format_content = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })

        # write model`s name as title
        count_field = len(list_fields)
        width_title = count_field if count_field > 3 else 4
        title_text = _("An exported data from the model \"{0}\"").format(model_name)
        sheet1.merge_range(1, 0, 2, width_title, title_text, format_title)

        # write numeration and label of column numeration "№"
        list_numbers_objects = tuple(range(qs.count()))
        cell_start_numeration = 'A6'
        cell_end_numeration = 'A{0}'.format(5 + len(list_numbers_objects))

        sheet1.write('A5', '№', format_sign_numeration)
        sheet1.write_column(cell_start_numeration, list_numbers_objects, format_content)

        # write formula
        cell_formula = 'A{0}'.format(6 + len(list_numbers_objects))
        formula = '={0}'.format(cell_end_numeration)
        sheet1.write_formula(cell_formula, formula, format_total_count_objects)

        # write field name
        for col_num, field_name in enumerate(list_fields):

            # start from 1
            col_num += 1

            field = model._meta.get_field(field_name)
            verbose_field_name = str(field.verbose_name)

            count_rows = self._get_count_rows(verbose_field_name)
            width_column = self._get_column_width(verbose_field_name)

            dict_rows_rows[4].add(count_rows)
            dict_columns_width[col_num].add(count_rows)

            sheet1.write(4, col_num, verbose_field_name, format_field_name)

        # write data
        for row_num, values_fields in enumerate(qs.values_list(*list_fields)):
            row_num += 5
            for col_num, field_name in enumerate(list_fields):
                value = values_fields[col_num]
                col_num += 1
                try:

                    #
                    if isinstance(value, datetime.datetime):
                        value = value.strftime('%H:%M:%S %d / %m / %Y')
                    elif isinstance(value, datetime.date):
                        value = value.strftime('%d / %m / %Y')
                    elif isinstance(value, uuid.UUID):
                        value = 'UUID({0})'.format(value)

                    count_rows = self._get_count_rows(value)
                    dict_rows_rows[row_num].add(count_rows)

                    width_column = self._get_column_width(value)
                    dict_columns_width[col_num].add(width_column)

                    #
                    sheet1.write(row_num, col_num, value, format_content)

                except TypeError as e:
                    sheet1.write(row_num, col_num, str(e))

        # set a count rows in all rows
        for row_num, set_count_rows in dict_rows_rows.items():
            # choice max count rows for pretty visible
            sheet1.set_row(row_num, max(set_count_rows))

        # set a width for all columns
        for col_num, set_width in dict_columns_width.items():
            # choice max width for pretty visible
            sheet1.set_column(col_num, col_num, max(set_width))

        # close workbook
        workbook.close()

        # get a xlsx data from the file and to write it in the HttpResponse
        xlsx_data = output.getvalue()
        response.write(xlsx_data)

        return response

    def _get_count_rows(self, value):

        if len(value) > 50:

            # split text on rows by \n
            # in each row must be not more 50 characters
            value = textwrap.fill(value, 20)

            # count character \n in text
            count_rows = value.count('\n')

            # determinate count rows for Excel, for incremente count_rows on 1.
            # considering what single row have height is 15, then make multiplication count rows on 15
            count_rows = (count_rows + 1) * 15
            return count_rows
        return 15

    def _get_column_width(self, value):

        #
        len_val = len(value)

        if len_val > 50:
            width_column = 51
        else:
            a = divmod(len_val, 8.43)
            width_column = math.floor(8.43 * a[0] + a[1])
        return width_column
