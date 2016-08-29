
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

# from apps.generic_models.admin import OpinionGenericInline, CommentGenericInline

from .models import UtilityCategory, Utility


class UtilityInline(admin.StackedInline):
    """
    Stacked Inline View for Utility
    """

    model = Utility
    extra = 1
    fk_name = 'category'


class UtilityCategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for UtilityCategory
    '''

    list_display = (
        'name',
        'get_count_utilities',
        'get_total_mark',
        'get_total_opinions',
        'get_total_comments',
        'is_new',
        'date_modified',
        'date_added')
    list_filter = ('date_modified', 'date_added')
    inlines = [
        UtilityInline,
    ]
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super(UtilityCategoryAdmin, self).get_queryset(request)
        qs = qs.categories_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                UtilityCategory._meta.verbose_name, {
                    'fields': [
                        'name',
                        'description',
                        'image',
                    ]
                }
            ]
        ]

        if obj:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        ''
                    ]
                }
            ])
        return fieldsets

    def get_inlines_instances(self, request, obj=None):

        if obj and obj.utilities.exists():
            inlines = []
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []


class UtilityAdmin(admin.ModelAdmin):
    '''
        Admin View for Utility
    '''

    list_display = (
        'name',
        'category',
        'get_mark',
        # 'get_count_opinions',
        # 'get_count_comments',
        'is_new',
        'date_modified',
        'date_added')
    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('name',)
    inlines = [
        # OpinionGenericInline,
        # CommentGenericInline,
    ]
    fieldsets = [
        [
            Utility._meta.verbose_name, {
                'fields': ['name', 'category', 'web_link', 'image', 'description']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(UtilityAdmin, self).get_queryset(request)
        qs = qs.utilities_with_all_additional_fields()
        return qs
