
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django import template

from mylabour.model_utils import get_string_primary_keys_separated_commas


register = template.Library()


@register.simple_tag(takes_context=True)
def make_url_for_export_data_model(context):

    opts = context['opts']
    contenttype_model = ContentType.objects.get_for_model(opts.model)

    # get a ChangeList object
    cl = context['cl']

    # get a current queryset in the ChangeList
    queryset = cl.queryset

    if not queryset:
        return '#'

    pks_separated_commas = get_string_primary_keys_separated_commas(queryset)

    return reverse(
        'export_import_models:export',
        kwargs={
            'contenttype_model_pk': contenttype_model.pk,
            'pks_separated_commas': pks_separated_commas,
        })
