
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from .models import ProgrammingUtility


class ProgrammingUtilityInline(admin.StackedInline):
    """
    Stacked Inline View for ProgrammingUtility
    """

    model = ProgrammingUtility
    extra = 1
    fk_name = 'category'


class ProgrammingCategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for ProgrammingCategory
    '''

    list_display = ('name', 'picture', 'get_count_programming_utilities', 'is_new', 'date_modified', 'date_added')
    list_filter = ('date_modified', 'date_added')
    inlines = [
        ProgrammingUtilityInline,
    ]
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super(ProgrammingCategoryAdmin, self).get_queryset(request)
        qs = qs.annotate(count_utilities=Count('programming_utilities'))
        return qs

    def get_count_programming_utilities(self, obj):
        return obj.count_utilities
    get_count_programming_utilities.admin_order_field = 'count_utilities'
    get_count_programming_utilities.short_description = _('Count utilities')


class ProgrammingUtilityAdmin(admin.ModelAdmin):
    '''
        Admin View for ProgrammingUtility
    '''

    list_display = ('name', 'category', 'is_new', 'date_modified', 'date_added')
    list_editable = ['category']
    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('name',)
