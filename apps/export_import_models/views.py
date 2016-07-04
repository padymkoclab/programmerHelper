
import csv

from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve
# from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, TemplateView
from django.core import serializers

from config.admin import ProgrammerHelperAdminSite

from .utils import get_filename_by_datetime_name_and_extension


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


class ExportPreviewView(View):
    """

    """

    def dispatch(self, request, *args, **kwargs):

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

        # make serializaion got the objects
        serializers.serialize(format_output, qs, stream=response, fields=list_fields)

        # if need return file (download), not preview
        mode = kwargs['mode']
        if mode == 'download':
            filename = get_filename_by_datetime_name_and_extension(
                name=model._meta.verbose_name_plural,
                extension=file_ext,
            )
            response['Content-Disposition'] = 'attachment;filename=' + filename

        return response


class ExportFile(View):

    def dispatch(self, request, *args, **kwargs):

        raise NotImplementedError

        return super(ExportFile, self).dispatch(request, *args, **kwargs)


class ExportCSV(View):
    """ """

    def dispatch(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        filename = get_filename_by_datetime_name_and_extension(name='', extension='csv')
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
        return response
