
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext


def delete_selected(model_admin, request, queryset):

    if not model_admin.has_delete_permission(request):
        raise PermissionDenied

    count = queryset.count()
    queryset.delete()

    if count > 1:
        object_name = model_admin.model._meta.verbose_name_plural
    elif count == 1:
        object_name = model_admin.model._meta.verbose_name

    object_name = object_name.lower()

    msg = ungettext(
        'Succefully deleted {} {}',
        'Succefully deleted {} {}',
        count
    ).format(count, object_name)

    messages.add_message(request, messages.SUCCESS, msg, extra_tags='deleted')


delete_selected.short_description = _('Delete selected {}')
