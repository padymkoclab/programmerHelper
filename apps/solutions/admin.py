
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.listfilters import IsNewSimpleListFilter
from utils.django.admin_utils import listing_objects_with_admin_url

from apps.core.admin import AppAdmin
from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from .forms import SolutionAdminModelForm
from .models import Solution


class SolutionAppAdmin(AppAdmin):

    def get_context_for_tables_of_statistics(self):
        """Add statictis data to a context."""

        return (
            (
                _('Solutions'), (
                    ('Count solutions', Solution.objects.count()),
                ),
            ),
            (
                _('Comments'), (
                    ('Average count comments', Solution.comments_manager.get_avg_count_comments()),
                    ('Count comments', Solution.comments_manager.get_count_comments()),
                    (_('Count distinct users posted comments'),
                        Solution.comments_manager.get_count_distinct_users_posted_comments()),
                ),
            ),
            (
                _('Opinions'), (
                    ('Average count opinions', Solution.opinions_manager.get_avg_count_opinions()),
                    ('Count opinions', Solution.opinions_manager.get_count_opinions()),
                    ('Count critics', Solution.opinions_manager.get_count_critics()),
                    ('Count supporters', Solution.opinions_manager.get_count_supporters()),
                ),
            ),
            (
                _('Tags'), (
                    ('Average count tags', Solution.tags_manager.get_avg_count_tags()),
                    ('Count usaged tags', Solution.tags_manager.get_count_usaged_tags()),
                    ('Count unique usaged tags', Solution.tags_manager.get_count_unique_usaged_tags()),
                ),
            ),
        )

    def get_context_for_charts_of_statistics(self):
        """ """

        return (
            {
                'title': _('Chart count solutions for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count solutions')),
                    'data': Solution.objects.get_statistics_count_solutions_for_the_past_year(),
                },
                'chart': Solution.objects.get_chart_count_solutions_for_the_past_year(),
            },
            {
                'title': _('Chart count opinions for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Total count opinions'), _('Coutn critics'), _('Count supporters')),
                    'data': Solution.opinions_manager.get_statistics_count_opinions_for_the_past_year(),
                },
                'chart': Solution.opinions_manager.get_chart_count_opinions_for_the_past_year(),
            },
            {
                'title': _('Chart count comments for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count comments')),
                    'data': Solution.comments_manager.get_statistics_count_comments_for_the_past_year(),
                },
                'chart': Solution.comments_manager.get_chart_count_comments_for_the_past_year(),
            },
        )

    def add_context_to_report_page(self, context):

        # context with statictis data
        context['themes_for_reports'] = {
            Solution._meta.verbose_name_plural: 'solutions',
        }

    def get_report(self, output_report, themes):

        msg = 'Report must generated in {0} on themes: {1}'.format(output_report.upper(), themes)
        return msg


class SolutionAdmin(admin.ModelAdmin):
    """
    Admin View for Solution
    """

    list_display = (
        'problem',
        'user',
        'get_rating',
        'get_count_opinions',
        'get_count_comments',
        'get_count_tags',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    search_fields = ('problem', )
    date_hierarchy = 'date_added'
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ['problem']}
    form = SolutionAdminModelForm
    readonly_fields = [
        'get_rating',
        'get_count_opinions',
        'get_count_comments',
        'get_count_tags',
        'date_modified',
        'date_added',
        'get_count_critics',
        'get_count_supporters',
        'get_listing_critics',
        'get_listing_supporters',
    ]

    def get_queryset(self, request):
        qs = super(SolutionAdmin, self).get_queryset(request)
        qs = qs.solutions_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Solution._meta.verbose_name, {
                    'fields': [
                        'problem',
                        'slug',
                        'user',
                        'body',
                        'tags',
                    ],
                }
            ],
        ]

        if obj is not None:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_rating',
                        'get_count_opinions',
                        'get_count_critics',
                        'get_count_supporters',
                        'get_listing_critics',
                        'get_listing_supporters',
                        'get_count_comments',
                        'get_count_tags',
                        'date_modified',
                        'date_added',
                    ]
                }
            ])

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            inlines = [OpinionGenericInline, CommentGenericInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def get_ordering(self, request):

        # ordering on base dynamic fields
        return ['-rating', '-count_opinions']

    def suit_row_attributes(self, obj, request):

        if obj.rating is not None:
            if obj.rating > 0:
                return {'class': 'success', 'data': obj.problem}
            elif obj.rating < 0:
                return {'class': 'error', 'data': obj.problem}

    def suit_cell_attributes(self, obj, column):

        if column in [
            'get_rating',
            'get_count_opinions',
            'get_count_comments',
            'get_count_tags',
            'is_new'
        ]:
            return {'class': 'text-center'}

        if column in [
            'date_modified',
            'date_added',
        ]:
            return {'class': 'text-right'}

    def get_listing_critics(self, obj):
        return listing_objects_with_admin_url(
            obj.get_critics(), 'get_admin_url', 'get_full_name', _('No body')
        )
    get_listing_critics.short_description = _('Critics')

    def get_listing_supporters(self, obj):

        return listing_objects_with_admin_url(
            obj.get_supporters(), 'get_admin_url', 'get_full_name', _('No body')
        )
    get_listing_supporters.short_description = _('Supporters')
