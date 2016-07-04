
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse
from django.core import serializers


def export_as_json(modeladmin, request, queryset):
    """ """

    response = HttpResponse(content_type='application/json')
    serializers.serialize('json', queryset, stream=response)
    return response
export_as_json.short_description = _('Export model in JSON file')


def export_as_xml(modeladmin, request, queryset):
    """ """

    response = HttpResponse(content_type='application/xml')
    serializers.serialize('xml', queryset, stream=response)
    return response
export_as_xml.short_description = _('Export model in XML file')


def export_as_yaml(modeladmin, request, queryset):
    """ """

    # This serializer is only available if PyYAML is installed.

    response = HttpResponse(content_type='application/yaml')
    serializers.serialize('yaml', queryset, stream=response)
    return response
export_as_yaml.short_description = _('Export model in YAML file')


def advanced_export(modeladmin, request, queryset):
    """ """

    # list primary keys selected objects
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

    # ContentType model of the selected objects
    ct_model = ContentType.objects.get_for_model(queryset.model)

    # url
    url = reverse(
        'export_import_models:admin_export',
        kwargs={'ct_model_pk': ct_model.pk, 'objects_pks': ','.join(selected)}
    )

    #
    return HttpResponseRedirect(url)
advanced_export.short_description = _('Export selected')
