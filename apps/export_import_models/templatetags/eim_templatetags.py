
from django.core.urlresolvers import reverse
from django import template

from mylabour.model_utils import get_string_primary_keys_separated_commas


register = template.Library()


@register.simple_tag(takes_context=True)
def make_url_for_export_data_model(context):

    opts = context['opts']
    app_label, model_name = opts.app_label, opts.model_name

    cl = context['cl']
    queryset = cl.queryset
    pks_separated_commas = get_string_primary_keys_separated_commas(queryset)

    return reverse(
        'export_import_models:export_model',
        kwargs={
            'app_label': app_label,
            'model_name': model_name,
            'pks_separated_commas': pks_separated_commas,
        })
