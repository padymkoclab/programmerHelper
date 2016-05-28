
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

# from apps.app_generic_models.admin import OpinionGenericInline, CommentGenericInline

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
        'picture',
        'views',
        'get_count_utilities',
        'get_total_scope',
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
    fieldsets = [
        [
            UtilityCategory._meta.verbose_name, {
                'fields': ['name', 'description', 'picture']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(UtilityCategoryAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_utilities=Count('utilities', distinct=True),
        )
        return qs

    def get_count_utilities(self, obj):
        return obj.count_utilities
    get_count_utilities.admin_order_field = 'count_utilities'
    get_count_utilities.short_description = _('Count utilities')


class UtilityAdmin(admin.ModelAdmin):
    '''
        Admin View for Utility
    '''

    list_display = (
        'name',
        'category',
        'get_scope',
        'get_count_opinions',
        'get_count_comments',
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
                'fields': ['name', 'category', 'web_link', 'picture', 'description']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(UtilityAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_opinions=Count('opinions', distinct=True),
            count_comments=Count('comments', distinct=True),
        )
        return qs

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')
