
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def clean_weblinks(form_instance):
    links = form_instance.cleaned_data['links']
    if not settings.MIN_COUNT_WEBLINKS_ON_OBJECT <= len(links) <= settings.MAX_COUNT_WEBLINKS_ON_OBJECT:
        msg = _('{0} may have from {1} to {2} links.').format(
            form_instance.Meta.model._meta.verbose_name,
            settings.MIN_COUNT_WEBLINKS_ON_OBJECT,
            settings.MAX_COUNT_WEBLINKS_ON_OBJECT,
        )
        form_instance.add_error('links', msg)
    return links
