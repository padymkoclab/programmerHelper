
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class IsCompletedSimpleListFilter(admin.SimpleListFilter):

    title = _('Is completed?')
    parameter_name = 'status_completeness'

    def lookups(self, request, model_admin):

        return (
            ('completed', _('Completed')),
            ('uncompleted', _('Uncompleted')),
        )

    def queryset(self, request, queryset):

        queryset = queryset.questions_with_status_completeness()
        if self.value() == 'completed':
            return queryset.filter(status_completeness=True)
        elif self.value() == 'uncompleted':
            return queryset.filter(status_completeness=False)
