
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext


def make_users_as_non_superuser(self, request, queryset):
    """Admin action by selected users will be non-superusers."""
    for obj in queryset:
        obj.is_superuser = False
        obj.save()
    message = ungettext(
        'Succefull update parametrs one user',
        'Succefull update parametrs %(count_users)d users',
        len(queryset)
    ) % {
        'count_users': len(queryset),
    }
    self.message_user(request, message)
make_users_as_non_superuser.short_description = _('Make selected users as non-superuser')


def make_users_as_superuser(self, request, queryset):
    """Admin action by selected users will be superusers."""
    for obj in queryset:
        obj.is_superuser = True
        obj.save()
    message = ungettext(
        'Succefull update parametrs one user',
        'Succefull update parametrs %(count_users)d users',
        len(queryset)
    ) % {
        'count_users': len(queryset),
    }
    self.message_user(request, message)
make_users_as_superuser.short_description = _('Make selected users as superuser')


def make_users_as_non_active(self, request, queryset):
    """Admin action by selected users will be non-superusers."""
    for obj in queryset:
        obj.is_active = False
        obj.save()
    message = ungettext(
        'Succefull update parametrs one user',
        'Succefull update parametrs %(count_users)d users',
        len(queryset)
    ) % {
        'count_users': len(queryset),
    }
    self.message_user(request, message)
make_users_as_non_active.short_description = _('Make selected users as non-active')


def make_users_as_active(self, request, queryset):
    """Admin action by selected users will be superusers."""
    for obj in queryset:
        obj.is_active = True
        obj.save()
    message = ungettext(
        'Succefull update parametrs one user',
        'Succefull update parametrs %(count_users)d users',
        len(queryset)
    ) % {
        'count_users': len(queryset),
    }
    self.message_user(request, message)
make_users_as_active.short_description = _('Make selected users as active')
