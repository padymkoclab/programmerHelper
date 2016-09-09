
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.listfilters import IsNewSimpleListFilter
from utils.django.admin_utils import listing_objects_with_admin_url

from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from .forms import SolutionAdminModelForm
from .models import Solution


class SolutionAppAdmin:

    def add_statistics_data_to_context(self, context):
        """Add statictis data to a context."""

        context['statistics_data'] = {
            'count_solutions': Solution.objects.count(),
            'avg_count_tags': Solution.objects.get_avg_count_tags(),
            'count_usaged_tags': Solution.objects.get_count_usaged_tags(),
            'count_unique_usaged_tags': Solution.objects.get_count_unique_usaged_tags(),
            'avg_count_comments': Solution.objects.get_avg_count_comments(),
            'avg_count_opinions': Solution.objects.get_avg_count_opinions(),
            'count_opinions': Solution.objects.get_count_opinions(),
            'count_comments': Solution.objects.get_count_comments(),
            'count_critics': Solution.objects.get_count_critics(),
            'count_supporters': Solution.objects.get_count_supporters(),
            'statistics_count_comments_for_the_past_year':
                Solution.objects.get_statistics_count_comments_for_the_past_year(),
            'statistics_count_opinions_for_the_past_year':
                Solution.objects.get_statistics_count_opinions_for_the_past_year(),
            'statistics_count_solutions_for_the_past_year':
                Solution.objects.get_statistics_count_solutions_for_the_past_year(),
            'chart_count_comments_for_the_past_year':
                Solution.objects.get_chart_count_comments_for_the_past_year(),
            'chart_count_opinions_for_the_past_year':
                Solution.objects.get_chart_count_opinions_for_the_past_year(),
            'chart_count_solutions_for_the_past_year':
                Solution.objects.get_chart_count_solutions_for_the_past_year(),
        }

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
        'get_mark',
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
        'get_mark',
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
                        'get_mark',
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
        return ['-mark', '-count_opinions']

    def suit_row_attributes(self, obj, request):
        if obj.mark > 0:
            return {'class': 'success', 'data': obj.problem}
        elif obj.mark < 0:
            return {'class': 'error', 'data': obj.problem}

    def suit_cell_attributes(self, obj, column):

        if column in [
            'get_mark',
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
