
import logging

from django.utils.text import force_text
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.listfilters import IsNewSimpleListFilter

from apps.core.admin import AppAdmin, AdminSite
from apps.opinions.admin import OpinionGenericInline
from apps.opinions.admin_mixins import OpinionsAdminMixin
from apps.comments.admin import CommentGenericInline

from .apps import UtilitiesConfig
from .models import Category, Utility
from .forms import CategoryAdminModelForm, UtilityAdminModelForm


logger = logging.getLogger('django.development')


@AdminSite.register_app_admin_class
class UtilitiesAppAdmin(AppAdmin):

    label = UtilitiesConfig.label

    def get_context_for_tables_of_statistics(self):
        """ """

        return (
            (
                _('Categories'), (
                    (_('Count categories'), Category.objects.count()),
                    (_('Average count utilities'), Category.objects.get_avg_count_utilities()),
                ),
            ),
            (
                _('Utilities'), (
                    (_('Count utilities'), Utility.objects.count()),
                )
            ),
            (
                _('Opinions'), (
                    (_('Average count opinions'), Utility.opinions_manager.get_avg_count_opinions()),
                    (_('Count opinions'), Utility.opinions_manager.get_count_opinions()),
                    (_('Count critics'), Utility.opinions_manager.get_count_critics()),
                    (_('Count supporters'), Utility.opinions_manager.get_count_supporters()),
                )
            ),
            (
                _('Comments'), (
                    (_('Count comments'), Utility.comments_manager.get_count_comments()),
                    (_('Average count comments'), Utility.comments_manager.get_avg_count_comments()),
                    (_('Count disticnt users posted comments'),
                        Utility.comments_manager.get_count_distinct_users_posted_comments()),
                )
            ),
        )

    def get_context_for_charts_of_statistics(self):
        """ """

        return (
            {
                'title': _('Chart count opinions for the past year'),
                'table': {
                    'fields': (
                        _('Month, year'),
                        _('Total count opinions'),
                        _('Count critical opinions'),
                        _('Count supporting opinions'),
                    ),
                    'data': Utility.opinions_manager.get_statistics_count_opinions_for_the_past_year(),
                },
                'chart': Utility.opinions_manager.get_chart_count_opinions_for_the_past_year(),
            },
            {
                'title': _('Chart count comments for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count comments')),
                    'data': Utility.comments_manager.get_statistics_count_comments_for_the_past_year(),
                },
                'chart': Utility.comments_manager.get_chart_count_comments_for_the_past_year(),
            },
        )

    def add_context_to_report_page(self, context):

        # context with statictis data
        context['themes_for_reports'] = {
            Category._meta.verbose_name_plural: 'categories',
            Utility._meta.verbose_name_plural: 'utilities',
        }

    def get_report(self, output_report, themes):

        msg = 'Report must generated in {0} on themes: {1}'.format(output_report.upper(), themes)
        return msg


class UtilityInline(admin.StackedInline):
    """
    Stacked Inline View for Utility
    """

    form = UtilityAdminModelForm
    model = Utility
    extra = 0
    fk_name = 'category'
    readonly_fields = ['get_rating', 'get_count_comments', 'get_count_opinions', 'updated', 'created']
    fields = [
        'name',
        'description',
        'category',
        'web_link',
        'get_rating',
        'get_count_comments',
        'get_count_opinions',
        'updated',
        'created',
    ]


@admin.register(Category, site=AdminSite)
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
        'updated',
        'created')
    list_filter = (
        IsNewSimpleListFilter,
        'updated',
        'created',
    )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = [
        'get_total_mark',
        'get_total_count_opinions',
        'get_total_count_comments',
        'get_count_utilities',
        'updated',
        'created',
    ]

    def get_queryset(self, request):

        qs = super().get_queryset(request)
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
                        'updated',
                        'created',
                    ]
                }
            ])
        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [UtilityInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []


@admin.register(Utility, site=AdminSite)
class UtilityAdmin(OpinionsAdminMixin, admin.ModelAdmin):
    '''
    Admin View for Utility
    '''

    form = UtilityAdminModelForm
    list_display = (
        'truncated_name',
        'category',
        'get_rating',
        'get_count_opinions',
        'get_count_comments',
        'is_new',
        'updated',
        'created',
    )

    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
        IsNewSimpleListFilter,
        'updated',
        'created',
    )
    search_fields = ('name', )
    readonly_fields = [
        'get_rating',
        'get_count_comments',
        'get_count_opinions',
        'get_count_critics',
        'get_count_supporters',
        'get_listing_critics_with_admin_urls',
        'get_listing_supporters_with_admin_urls',
        'updated',
        'created',
    ]

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
                        'get_rating',
                        'get_count_comments',
                        'get_count_opinions',
                        'get_count_critics',
                        'get_count_supporters',
                        'get_listing_critics_with_admin_urls',
                        'get_listing_supporters_with_admin_urls',
                        'updated',
                        'created',
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

    def suit_cell_attributes(self, obj, column):

        if column in ['truncated_name', 'category']:
            css_class = 'text-left'
        elif column in ['created', 'updated']:
            css_class = 'text-right'
        else:
            css_class = 'text-center'

        return {'class': css_class}

    def suit_row_attributes(self, obj, request):

        if obj.rating is not None:
            if obj.rating > 0:
                return {'class': 'success'}
            elif obj.rating < 0:
                return {'class': 'error'}

    def truncated_name(self, obj):
        return truncatechars(force_text(obj), 50)
    truncated_name.short_description = Utility._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'
