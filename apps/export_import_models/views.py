
from io import BytesIO, StringIO
import warnings
import itertools
import csv

from django.template import Template, Context
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve
# from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest, StreamingHttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, TemplateView
from django.core import serializers

from config.admin import ProgrammerHelperAdminSite

from reportlab.pdfgen import canvas
import xlsxwriter
import xlwt
import xlrd

from .utils import get_filename_by_datetime_name_and_extension


def made_validation(kwargs):

    # get model
    ct_model_pk = int(kwargs['ct_model_pk'])
    try:
        ct_model = ContentType.objects.get(pk=ct_model_pk)
    except:
        return HttpResponseBadRequest(_('Not prossible get a data from the database. Corrupted input the data.'))
    model = ct_model.model_class()

    # get objects of model
    objects_pks = kwargs['objects_pks']
    list_objects_pks = objects_pks.split(',')
    try:
        qs = model.objects.filter(pk__in=list_objects_pks)
        qs.count()
    except:
        return HttpResponseBadRequest(_('Not prossible get a data from the database. Corrupted input the data.'))

    # compare count got and requested the objects
    if len(list_objects_pks) != len(qs):
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


class ExportTemplateView(TemplateView):
    """ """

    template_name = "export_import_models/admin/export.html"

    def dispatch(self, request, *args, **kwargs):

        #
        kwargs = self.request.resolver_match.kwargs

        #
        ct_model_pk = kwargs['ct_model_pk']
        ct_model = ContentType.objects.get(pk=ct_model_pk)
        model = ct_model.model_class()

        #
        objects_pks = kwargs['objects_pks']
        list_objects_pks = objects_pks.split(',')

        #
        try:
            count_objects = model.objects.filter(pk__in=list_objects_pks).count()
        except ValueError:
            raise HttpResponseBadRequest(_('Not prossible get a data from the database. Corrupted input the data.'))

        #
        if len(list_objects_pks) != count_objects:
            raise HttpResponseBadRequest(_('A data were corrupted. Not all a primary key of the objects has in database.'))

        # For only admin theme Django-Suit
        # It need namespace for display menu in left sidebar
        request.current_app = resolve('/admin/').namespace

        return super(ExportTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExportTemplateView, self).get_context_data(**kwargs)

        #
        ct_model_pk = kwargs['ct_model_pk']
        ct_model = ContentType.objects.get(pk=ct_model_pk)
        model = ct_model.model_class()

        #
        objects_pks = kwargs['objects_pks']
        # list_objects_pks = objects_pks.split(',')
        # objects = model.objects.filter(pk__in=list_objects_pks)

        #
        context['ct_model_pk'] = ct_model_pk
        context['fields'] = model._meta.fields
        context['objects_pks'] = objects_pks
        context['count_objects'] = len(objects_pks.split(','))

        context.update(ProgrammerHelperAdminSite.each_context(self.request))

        return context


class ExportPreviewDownloadView(View):
    """

    """

    def dispatch(self, request, *args, **kwargs):

        response = made_validation(kwargs)
        if isinstance(response, HttpResponseBadRequest):
            return response
        model, qs, list_fields = response

        # choice correct content_type for HttpResponse
        format_output = kwargs['format']
        if format_output == 'json':
            content_type = 'text/json'
            file_ext = 'json'
        elif format_output == 'xml':
            content_type = 'text/xml'
            file_ext = 'xml'
        else:
            content_type = 'text/x-yaml'
            file_ext = 'yaml'
        response = HttpResponse(content_type=content_type)

        # make serializaion got the objects
        serializers.serialize(format_output, qs, stream=response, fields=list_fields)

        # if need return file (download), not preview
        mode = kwargs['mode']
        if mode == 'download':
            filename = get_filename_by_datetime_name_and_extension(
                name=model._meta.verbose_name_plural,
                extension=file_ext,
            )
            response['Content-Disposition'] = 'attachment;filename="%s"' % filename

        return response


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
        filename = get_filename_by_datetime_name_and_extension(name=model._meta.verbose_name_plural, extension='csv')

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
        response = made_validation(kwargs)
        if isinstance(response, HttpResponseBadRequest):
            return response
        model, qs, list_fields = response
        filename = get_filename_by_datetime_name_and_extension(name=model._meta.verbose_name_plural, extension='xls')

        return self.import_from_xsl_with_xlrd()
        return self.generate_excel_with_XlsxWriter(model, qs, list_fields, filename)
        return self.generate_excel_with_xlwt(model, qs, list_fields, filename)
        # return self.generate_csv_simple(model, qs, list_fields, filename)

    def import_from_xsl_with_xlrd(self):

        response = HttpResponse()

        book = xlrd.open_workbook('/home/wlysenko/.virtualenvs/virtual_programmerHelper/project_programmerHelper/test.xls')
        response.write('<br />Count sheets: %d' % book.nsheets)
        first_sheet = book.sheet_by_index(0)
        response.write('<br />Sheet1-Row1: %s\n' % first_sheet.row_values(0))
        response.write('<br />Sheet1-Row1-Cell - 0, 0: %s\n' % first_sheet.cell(0, 0))
        return response

    def generate_excel_with_xlwt(self, model, qs, list_fields, filename):
        """ """

        # file:///media/wlysenko/66ABF2AC3D03BAAA/Web/Sites_info/MousePython/Creating%20Microsoft%20Excel%20Spreadsheets%20with%20Python%20and%20xlwt%20_%20The%20Mouse%20Vs.%20The%20Python.html

        response = HttpResponse(content_type='application/application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename

        #
        output = StringIO()
        book = xlwt.Workbook(output)
        sheet1 = book.add_sheet("PySheet1")
        cols = ["A", "B", "C", "D", "E"]
        txt = "Row %s, Col %s"

        for num in range(5):
            row = sheet1.row(num)
            for index, col in enumerate(cols):
                value = txt % (num + 1, col)
                row.write(index, value)

        #
        # book.close()
        response.write(output.getvalue())

        return response

    def generate_excel_with_XlsxWriter(self, model, qs, list_fields, filename):
        """ """

        # file:///media/wlysenko/66ABF2AC3D03BAAA/Web/Sites_info/How%20to%20export%20Excel%20files%20in%20a%20Python_Django%20application%20_%20ASSIST%20Software%20Romania.html

        response = HttpResponse(content_type='application/application/vnd.ms-excel')
        # made extension as .xlsx ( + 'x' to end)
        filename = filename + 'x'
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename

        #
        output = StringIO()
        workbook = xlsxwriter.Workbook(output)

        #
        worksheet_s = workbook.add_worksheet("Summary")
        title = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        })
        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })
        title_text = "{0} {1}".format("Weather History for", 'town_text')
        worksheet_s.merge_range('B2:H2', title_text, title)
        worksheet_s.write(4, 0, "No", header)
        worksheet_s.write(4, 1, "Town", header)
        worksheet_s.write(4, 3, "Max T. (℃)", header)
        # # the rest of the headers from the HTML file

        #
        workbook.close()

        #
        xlsx_data = output.getvalue()
        response.write(xlsx_data)

        return response


class ExportPDF(View):
    """
    View for export data of a models to PDF
    """

    def generate_pdf_simple(self, filename):
        """ """

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        p = canvas.Canvas(response)
        p.drawString(400, 400, 'I am Python/JavaScript developer!')
        p.showPage()
        p.save()
        return response

    def generate_pdf_complex(self, filename):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        buffer_pdf = BytesIO()
        p = canvas.Canvas(buffer_pdf)

        p.drawString(100, 400, 'I am a programmer')
        p.showPage()
        p.save()

        pdf = buffer_pdf.getvalue()
        buffer_pdf.close()
        response.write(pdf)
        return response

    def dispatch(self, request, *args, **kwargs):

        #
        # response = made_validation(kwargs)
        # if isinstance(response, HttpResponseBadRequest):
        #     return response
        # model, qs, list_fields = response
        from apps.polls.models import Poll
        model = Poll
        filename = get_filename_by_datetime_name_and_extension(model._meta.verbose_name_plural, 'pdf')

        # return self.generate_pdf_simple(model, qs, list_fields, filename=filename)
        return self.generate_pdf_complex(filename=filename)
        return self.generate_pdf_simple(filename=filename)
