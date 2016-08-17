
import itertools

from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    StreamingHttpResponse,
    Http404,
    HttpResponseRedirect,
)
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, TemplateView
from django.core import serializers

import magic

from config.admin import AdminSite
from mylabour.utils import get_filename_with_datetime, create_logger_by_filename

from .forms import UploadSerializedFileForm


logger = create_logger_by_filename(__name__)


class ExportTemplateView(TemplateView):
    """
    View fo export data from a model in the admin.
    """

    template_name = "export_import_models/admin/export.html"

    def get(self, request, *args, **kwargs):

        # get a model and it a content type instance
        contenttype_model_pk = kwargs['contenttype_model_pk']
        self.contenttype_model = get_object_or_404(ContentType, pk=contenttype_model_pk)
        self.model = self.contenttype_model.model_class()

        # get pks of objects and convert it in a list
        self.pks_separated_commas = kwargs['pks_separated_commas']
        list_pks_separated_commas = self.pks_separated_commas.split(',')

        # raise Http404 if input primary keys of objects is corrupted
        # especially for UUID field
        try:
            self.queryset = self.model._default_manager.filter(pk__in=list_pks_separated_commas)
            count_objects = self.queryset.count()
        except ValueError:
            raise Http404(_('Not prossible get a data from the database. Corrupted input the data.'))

        # raise Http404 if not all passed primary keys of objects contains on db
        if len(list_pks_separated_commas) != count_objects:
            raise Http404(
                _('A data were corrupted. Not all a primary key of the objects has in database.'))

        # For only admin theme Django-Suit
        # It need namespace for display menu in left sidebar
        request.current_app = AdminSite.name

        return super(ExportTemplateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(ExportTemplateView, self).get_context_data(**kwargs)

        # context needed for serialization
        context['contenttype_model_pk'] = self.contenttype_model.pk
        context['fields'] = self._get_serialized_fields(self.model)
        context['queryset'] = self.queryset
        context['pks_separated_commas'] = self.pks_separated_commas

        # for access to the django.jQuery() on page
        context['django_admin_media'] = admin.ModelAdmin(get_user_model(), AdminSite).media

        # pass a title of the page
        model_verbose_name = self.model._meta.verbose_name
        context['title'] = _('Export data from the model "{0}"').format(model_verbose_name)

        context.update(AdminSite.each_context(self.request))

        return context

    def _get_serialized_fields(self, model):
        """Return fields of the model, possible to serialization"""

        # get all fields
        fields = model._meta.concrete_fields
        many_to_many_fields = model._meta.many_to_many

        # reject m2m fields thought intermediate model
        many_to_many_fields = filter(lambda field: field.remote_field.through._meta.auto_created, many_to_many_fields)

        # reject all non-serializatable fields
        fields = list(filter(lambda field: field.serialize, itertools.chain(fields, many_to_many_fields)))

        return fields


class ExportPreviewDownloadView(View):
    """
    View for export data in downloaded file or preview these data.
    """

    def get(self, request, *args, **kwargs):

        # supported formats for export data from models
        allowed_formats = ['json', 'yaml', 'xml', 'csv']

        # data from hidden inputs
        pks_separated_commas = request.GET.get('pks_separated_commas')
        contenttype_model_pk = request.GET.get('contenttype_model_pk')

        # data from a user
        format_export_data = request.GET.get('format_export_data',)
        fields = request.GET.getlist('fields')

        if format_export_data not in allowed_formats:
            return HttpResponseBadRequest('A passed format for export is not supported.')

        # get model`s instance contenttype and model
        contenttype_model = get_object_or_404(ContentType, pk=contenttype_model_pk)
        model = contenttype_model.model_class()

        # get list of primary keys of objects for export
        list_pks_separated_commas = pks_separated_commas.split(',')

        # get queryset of objects by their keys
        queryset = model._default_manager.filter(pk__in=list_pks_separated_commas)
        model_verbose_name = model._meta.verbose_name

        # since CSV response always doesn`t have ability for preview
        # change content_type of response to plain text
        if format_export_data == 'csv' and 'preview' in request.GET:
            content_type = 'text/plain'
        else:
            content_type = 'text/{0}'.format(format_export_data)

        # create a response
        response = HttpResponse(content_type=content_type)

        # get a filename with name of the model and a datetime it created
        filename = get_filename_with_datetime(model_verbose_name, format_export_data)

        # serialization
        serializer = serializers.get_serializer(format_export_data)
        serializer = serializer()
        serializer.serialize(queryset, stream=response, fields=fields)

        # attach a file to the response, if output should be downloaded
        if 'download' in request.GET:
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

        return response


class ImportTemplateView(TemplateView):

    template_name = "export_import_models/admin/import.html"

    valid_deserialized_objects = list()

    def dispatch(self, request, *args, **kwargs):

        # For only admin theme Django-Suit
        # It need namespace for display menu in left sidebar
        request.current_app = AdminSite.name

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

            self.valid_deserialized_objects = list()

            if form.is_valid():
                file = request.FILES['file']

                file_extension = file.name.rsplit('.')[-1]

                file_mimetype = magic.from_buffer(file.file.getvalue(), mime=True)

                if file_mimetype not in ['application/xml', 'text/plain']:
                    form.add_error('file', _('File must be xml, json, yaml or csv.'))
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

                context['details_import'] = dict(
                    verbose_application_name=verbose_application_name,
                    verbose_model_name=verbose_model_name,
                    format_file_for_import=format_file_for_import,
                    count_importing_objects=count_importing_objects,
                    count_valid_objects=count_valid_objects,
                )

            logger.info('User made import data in model')

            return render(request, self.template_name, context)

        elif 'submit_apply_import' in request.POST:

            for valid_deserialized_object in self.valid_deserialized_objects:
                valid_deserialized_object.full_clean()
                valid_deserialized_object.save()

            url_redirect = reverse('export_import_models:import_result')
            return HttpResponseRedirect(url_redirect)

    def get_context_data(self, **kwargs):
        context = super(ImportTemplateView, self).get_context_data(**kwargs)
        context['title'] = _('Import data in a model')

        return context


class ImportResultTemplateView(TemplateView):

    template_name = 'export_import_models/admin/import_result.html'
