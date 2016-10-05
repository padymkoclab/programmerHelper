
import logging

from django.utils.text import force_text
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.listfilters import IsNewSimpleListFilter

from apps.admin.admin import ModelAdmin

from apps.core.admin import AppAdmin, AdminSite
from apps.opinions.admin import OpinionGenericInline
from apps.opinions.admin_mixins import OpinionsAdminMixin
from apps.comments.admin import CommentGenericInline

from .apps import UtilitiesConfig
from .models import Category, Utility
from .forms import CategoryAdminModelForm, UtilityAdminModelForm


logger = logging.getLogger('django.development')


# @AdminSite.register_app_admin_class
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


# @admin.register(Category, site=AdminSite)
class CategoryAdmin(ModelAdmin):
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
        'created',
    )
    list_display_styles = (
        (
            ('__all__', ), {
                'align': 'center',
            },
        ),
        (
            ('name', ), {
                'align': 'left',
            },
        ),
        (
            ('updated', 'created'), {
                'align': 'right',
            },
        ),
    )
    colored_rows_by = 'determinate_color_rows'
    list_filter = (
        IsNewSimpleListFilter,
        'updated',
        'created',
    )
    list_per_page = 10
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
                    'description': _("""
                        I used to develop Django sites by running them on my OS X laptop locally and deploying to a
                        Linode VPS.
                        I had a whole section of this post written up about tricks and tips for working with that
                        setup."""
                                     ),
                    'classes': _('text-success ', ),
                    'fields': [
                        'name',
                        'slug',
                        'description',
                    ]
                }
            ]
        ]

        if obj is not None:
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

    def determinate_color_rows(self, obj):
        total_mark = obj.get_total_mark()

        row_color = None
        if total_mark is not None:
            if total_mark > 0:
                row_color = 'success'
            elif total_mark < 0:
                row_color = 'danger'

        return row_color


# @admin.register(Utility, site=AdminSite)
class UtilityAdmin(OpinionsAdminMixin, ModelAdmin):
    '''
    Admin View for Utility
    '''

    form = UtilityAdminModelForm
    list_display = (
        'name',
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
