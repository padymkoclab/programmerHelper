
from django.utils.translation import ugettext_lazy as _


def delete_unused_tags(model_admin, request, queryset):

    raise NotImplementedError
    queryset.delete()


delete_unused_tags.short_description = _('Delete unused tags')
