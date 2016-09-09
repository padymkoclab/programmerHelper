
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def clean_tags(form_instance):
    tags = form_instance.cleaned_data['tags']
    if not settings.MIN_COUNT_TAGS_ON_OBJECT <= len(tags) <= settings.MAX_COUNT_TAGS_ON_OBJECT:
        msg = _('{0} may has from {1} to {2} tags.').format(
            form_instance.Meta.model._meta.verbose_name,
            settings.MIN_COUNT_TAGS_ON_OBJECT,
            settings.MAX_COUNT_TAGS_ON_OBJECT,
        )
        form_instance.add_error('tags', msg)
    return tags
