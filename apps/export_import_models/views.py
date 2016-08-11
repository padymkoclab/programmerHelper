
import math
import textwrap
import datetime
from io import BytesIO
import warnings
import itertools
import csv
import collections
import uuid

from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest, StreamingHttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, TemplateView, RedirectView
from django.core import serializers

import xlsxwriter
import magic

from config.admin import ProgrammerHelperAdminSite
from mylabour.utils import get_filename_with_datetime, create_logger_by_filename

from .forms import UploadSerializedFileForm


logger = create_logger_by_filename(__name__)


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
                serializer.serialize(queryset, stream=response, fields=fields)

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

    valid_deserialized_objects = list()

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

        if 'submit_make_check_file' in request.POST:

            form = UploadSerializedFileForm(request.POST, request.FILES)
            context = self.get_context_data()
            context['form'] = form

            if form.is_valid():
                file = request.FILES['file']

                file_extension = file.name.rsplit('.')[-1]

                file_mimetype = magic.from_buffer(file.file.getvalue(), mime=True)

                if file_mimetype not in ['application/xml', 'text/plain']:
                    form.add_error('file', _('File must be xml, json or yaml.'))
                    return render(request, self.template_name, context)

                data = file.file.getvalue()

                # for UTF
                data = str(data, encoding='utf')

                deserialized_objects = serializers.deserialize(file_extension, data)

                lst = list()

                for num_obj, deserialized_object in enumerate(deserialized_objects):
                    obj = deserialized_object.object
                    obj_detail = dict(
                        pk=obj.pk,
                        str=str(obj),
                        is_valid=True,
                        errors='',
                    )
                    try:
                        obj.full_clean()
                        self.valid_deserialized_objects.append(obj)
                    except ValidationError as errors:
                        obj_detail['is_valid'] = False
                        obj_detail['errors'] = errors

                    lst.append(obj_detail)
                context['deserialized_objects'] = lst

                verbose_application_name = deserialized_object.object._meta.app_config.verbose_name
                verbose_model_name = deserialized_object.object._meta.verbose_name
                format_file_for_import = file_extension.upper()
                count_importing_objects = num_obj + 1
                count_valid_objects = len(self.valid_deserialized_objects)

                details_import = dict(
                    verbose_application_name=verbose_application_name,
                    verbose_model_name=verbose_model_name,
                    format_file_for_import=format_file_for_import,
                    count_importing_objects=count_importing_objects,
                    count_valid_objects=count_valid_objects,
                )
                context['details_import'] = details_import

            logger.info('User made import data in model')

            return render(request, self.template_name, context)

        elif 'submit_apply_import' in request.POST:

            for valid_deserialized_object in self.valid_deserialized_objects:
                valid_deserialized_object.save()

            url_redirect = reverse('export_import_models:import_result')
            return HttpResponseRedirect(url_redirect)

    def get_context_data(self, **kwargs):
        context = super(ImportTemplateView, self).get_context_data(**kwargs)
        context['title'] = _('Import data in a model')

        return context


class ImportResultTemplateView(TemplateView):

    template_name = 'export_import_models/admin/import_result.html'


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
