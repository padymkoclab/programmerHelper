
from unittest import mock

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.apps import apps
from django.utils.text import force_text
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.python.logging_utils import create_logger_by_filename
from utils.django.listfilters import IsNewSimpleListFilter

from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from .models import Category, Utility
from .forms import CategoryAdminModelForm, UtilityAdminModelForm


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


class CategoryAdmin(admin.ModelAdmin):
    '''
    Admin View for Category
    '''

    form = CategoryAdminModelForm
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

        qs = super(CategoryAdmin, self).get_queryset(request)
        qs = qs.categories_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Category._meta.verbose_name, {
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

    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
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


class UtilitiesAppAdmin:

    def add_statistics_data_to_context(self, context):
        """Add statictis data to a context."""

        context['statistics_data'] = {
            'count_categories': Category.objects.count(),
            'avg_count_utilities_in_categories': Category.objects.get_avg_count_utilities_in_categories(),
            'count_utilities': Utility.objects.count(),
            'avg_count_opinions_in_utilities': Utility.objects.get_avg_count_opinions_in_utilities(),
            'avg_count_comments_in_utilities': Utility.objects.get_avg_count_comments_in_utilities(),
            'count_opinions': Utility.objects.get_count_opinions(),
            'count_good_opinions': Utility.objects.get_count_good_opinions(),
            'count_bad_opinions': Utility.objects.get_count_bad_opinions(),
            'count_comments': Utility.objects.get_count_comments(),
            'count_users_posted_comments': Utility.objects.get_count_users_posted_comments(),
            'chart_most_popular_utilities': Utility.objects.get_chart_most_popular_utilities(),
            'most_popular_utilities': Utility.objects.get_most_popular_utilities(),
        }

    def add_context_to_report_page(self, context):

        # context with statictis data
        context['themes_for_reports'] = {
            Category._meta.verbose_name_plural: 'categories',
            Utility._meta.verbose_name_plural: 'utilities',
        }

    def get_report(self, output_report, themes):

        msg = 'Report must generated in {0} on themes: {1}'.format(output_report.upper(), themes)
        return msg
