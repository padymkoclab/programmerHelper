
from django.http import HttpResponse
from django.conf.urls import url
from django.utils.text import force_text
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from mylabour.logging_utils import create_logger_by_filename
from mylabour.listfilters import IsNewSimpleListFilter

from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from .models import UtilityCategory, Utility
from .forms import UtilityCategoryAdminModelForm, UtilityAdminModelForm


logger = create_logger_by_filename(__name__)


class UtilityInline(admin.StackedInline):
    """
    Stacked Inline View for Utility
    """

    form = UtilityAdminModelForm
    model = Utility
    extra = 0
    fk_name = 'category'
    readonly_fields = ['get_mark', 'get_count_comments', 'get_count_opinions', 'date_modified', 'date_added']
    fields = [
        'name',
        'description',
        'category',
        'web_link',
        'get_mark',
        'get_count_comments',
        'get_count_opinions',
        'date_modified',
        'date_added',
    ]


class UtilityCategoryAdmin(admin.ModelAdmin):
    '''
    Admin View for UtilityCategory
    '''

    form = UtilityCategoryAdminModelForm
    list_display = (
        'name',
        'get_count_utilities',
        'get_total_mark',
        'get_total_count_opinions',
        'get_total_count_comments',
        'is_new',
        'date_modified',
        'date_added')
    list_filter = (
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = [
        'get_total_mark',
        'get_total_count_opinions',
        'get_total_count_comments',
        'get_count_utilities',
        'date_modified',
        'date_added',
    ]

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
                        'slug',
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
                        'get_total_mark',
                        'get_total_count_opinions',
                        'get_total_count_comments',
                        'get_count_utilities',
                        'date_modified',
                        'date_added',
                    ]
                }
            ])
        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [UtilityInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def get_urls(self):

        urls = super().get_urls()

        additional_urls = [
            url(r'/admin/utilities/statistics/', self.statistics_view, {}, 'admin_utilities_statistics'),
        ]

        return additional_urls + urls

    def statistics_view(self, request):

        return HttpResponse('Nice')


class UtilityAdmin(admin.ModelAdmin):
    '''
    Admin View for Utility
    '''

    form = UtilityAdminModelForm
    list_display = (
        'truncated_name',
        'category',
        'get_mark',
        'get_count_opinions',
        'get_count_comments',
        'is_new',
        'date_modified',
        'date_added',
    )

    logger.error('Does not working (\'category\', admin.RelatedOnlyFieldListFilter),')

    list_filter = (
        # ('category', admin.RelatedOnlyFieldListFilter),
        # https://code.djangoproject.com/ticket/26979
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    search_fields = ('name', )
    readonly_fields = ['get_mark', 'get_count_comments', 'get_count_opinions', 'date_modified', 'date_added']

    def get_queryset(self, request):
        qs = super(UtilityAdmin, self).get_queryset(request)
        qs = qs.utilities_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Utility._meta.verbose_name, {
                    'fields': [
                        'name',
                        'description',
                        'category',
                        'web_link',
                    ]
                }
            ],
        ]

        if obj:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_mark',
                        'get_count_comments',
                        'get_count_opinions',
                        'date_modified',
                        'date_added',
                    ]
                }
            ])

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [
                OpinionGenericInline,
                CommentGenericInline,
            ]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def truncated_name(self, obj):
        return truncatechars(force_text(obj), 50)
    truncated_name.short_description = Utility._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'
