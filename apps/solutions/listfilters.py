
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class QualityListFilter(admin.SimpleListFilter):
    """
    ListFilter for django-admin for using for filter solutions by quality.
    """

    title = _('Quality')
    parameter_name = 'quality'

    def lookups(self, request, model_admin):
        return (
            ('wrong', _('Wrong')),
            ('bad', _('Bad')),
            ('vague', _('Vague')),
            ('good', _('Good')),
            ('approved', _('Approved')),
        )

    def queryset(self, request, queryset):
        queryset = queryset.solutions_with_qualities()
        if self.value() == 'wrong':
            return queryset.filter(quality='Wrong')
        elif self.value() == 'bad':
            return queryset.filter(quality='Bad')
        elif self.value() == 'vague':
            return queryset.filter(quality='Vague')
        elif self.value() == 'good':
            return queryset.filter(quality='Good')
        elif self.value() == 'approved':
            return queryset.filter(quality='Approved')
