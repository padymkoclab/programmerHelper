
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class StatusWebLinkListFilter(admin.SimpleListFilter):
    """
    Filter weblinks in admin by status: active, broken.
    """

    title = _('Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('broken', _('Broken')),
            ('active', _('Active')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'broken':
            queryset.weblinks_with_status().filter(status=False)
        elif self.value() == 'active':
            queryset.weblinks_with_status().filter(status=True)
