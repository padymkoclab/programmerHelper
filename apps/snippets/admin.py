
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.admin_utils import listing_objects_with_admin_url
from utils.django.listfilters import IsNewSimpleListFilter

from apps.core.admin import AppAdmin
from apps.comments.admin import CommentGenericInline
from apps.opinions.admin import OpinionGenericInline

from .apps import SnippetsConfig
from .models import Snippet
from .forms import SnippetAdminModelForm


class SnippetAppAdmin(AppAdmin):

    label = SnippetsConfig.label

    def get_context_for_tables_of_statistics(self):
        """Add statictis data to a context."""

        return (
            (
                _('Snippets'), (
                    (_('Count snippets'), Snippet.objects.count()),
                )
            ),
            (
                _('Comments'), (
                    (_('Average count comments'), Snippet.comments_manager.get_avg_count_comments()),
                    (_('Count comments'), Snippet.comments_manager.get_count_comments()),
                    (_('Count disticnt users posted comments'),
                        Snippet.comments_manager.get_count_distinct_users_posted_comments()),
                )
            ),
            (
                _('Opinions'), (
                    (_('Average count opinions'), Snippet.opinions_manager.get_avg_count_opinions()),
                    (_('Count opinions'), Snippet.opinions_manager.get_count_opinions()),
                    (_('Count critics'), Snippet.opinions_manager.get_count_critics()),
                    (_('Count supporters'), Snippet.opinions_manager.get_count_supporters()),
                )
            ),
            (
                _('Tags'), (
                    (_('Average count tags'), Snippet.tags_manager.get_avg_count_tags()),
                    (_('Count usaged tags'), Snippet.tags_manager.get_count_usaged_tags()),
                    (_('Count unique usaged tags'), Snippet.tags_manager.get_count_unique_usaged_tags()),
                )
            ),
        )

    def get_context_for_charts_of_statistics(self):
        """ """

        return (
            {
                'title': _('Chart count snippets for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count snippets')),
                    'data': Snippet.objects.get_statistics_count_snippets_for_the_past_year(),
                },
                'chart': Snippet.objects.get_chart_count_snippets_for_the_past_year(),
            },
            {
                'title': _('Chart count lexers for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count lexers')),
                    'data': Snippet.objects.get_statistics_usage_lexers(),
                },
                'chart': Snippet.objects.get_chart_statistics_usage_lexers(),
            },
            {
                'title': _('Chart count comments for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count comments')),
                    'data': Snippet.comments_manager.get_statistics_count_comments_for_the_past_year(),
                },
                'chart': Snippet.comments_manager.get_chart_count_comments_for_the_past_year(),
            },
            {
                'title': _('Chart count opinions for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count opinions')),
                    'data': Snippet.opinions_manager.get_statistics_count_opinions_for_the_past_year(),
                },
                'chart': Snippet.opinions_manager.get_chart_count_opinions_for_the_past_year(),
            },
        )

    def add_context_to_report_page(self, context):

        # context with statictis data
        context['themes_for_reports'] = {
            Snippet._meta.verbose_name_plural: 'snippets',
        }

    def get_report(self, output_report, themes):

        msg = 'Report must generated in {0} on themes: {1}'.format(output_report.upper(), themes)
        return msg


class SnippetAdmin(admin.ModelAdmin):
    '''
    Admin View for Snippet.
    '''

    form = SnippetAdminModelForm
    list_display = (
        'truncated_title',
        'user',
        'lexer',
        'get_rating',
        'get_count_tags',
        'get_count_opinions',
        'get_count_comments',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('lexer', admin.AllValuesFieldListFilter),
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )

    search_fields = ('title', )
    filter_horizontal = ['tags']
    date_hierarchy = 'date_added'

    readonly_fields = [
        'get_rating',
        'get_count_tags',
        'get_count_opinions',
        'get_count_comments',
        'date_modified',
        'date_added',
        'get_count_critics',
        'get_count_supporters',
        'get_listing_critics_with_admin_urls',
        'get_listing_supporters_with_admin_urls',
    ]

    def get_queryset(self, request):
        qs = super(SnippetAdmin, self).get_queryset(request)
        qs = qs.snippets_with_all_additional_fields()
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            inlines = [OpinionGenericInline, CommentGenericInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Snippet._meta.verbose_name, {
                    'fields': [
                        'title',
                        'slug',
                        'user',
                        'lexer',
                        'description',
                        'tags',
                    ]
                }
            ],
            [
                Snippet._meta.get_field('code').verbose_name, {
                    'classes': ('full-width', ),
                    'fields': ['code']
                }
            ]
        ]

        if obj is not None:

            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_count_tags',
                        'get_count_comments',
                        'get_count_opinions',
                        'get_rating',
                        'get_count_critics',
                        'get_count_supporters',
                        'get_listing_critics_with_admin_urls',
                        'get_listing_supporters_with_admin_urls',
                        'date_modified',
                        'date_added',
                    ],
                }
            ])

        return fieldsets

    def truncated_title(self, obj):
        return truncatechars(obj.title, 50)
    truncated_title.short_description = Snippet._meta.get_field('title').verbose_name
    truncated_title.admin_order_field = 'title'

    def suit_row_attributes(self, obj, request):

        if obj.rating is not None:
            if obj.rating < 0:
                return {'class': 'error'}
            elif obj.rating > 0:
                return {'class': 'success'}

    def suit_cell_attributes(self, obj, column):

        if column in ['truncated_title']:
            return {'class': 'text-left'}
        elif column in ['date_modified', 'date_added']:
            return {'class': 'text-right'}
        else:
            return {'class': 'text-center'}

    def preview_snippet(self):
        """ """

        raise NotImplementedError

    def get_listing_critics_with_admin_urls(self, obj):
        """ """

        return listing_objects_with_admin_url(
            obj.get_critics(),
            'get_admin_url',
            'get_full_name',
            _('No body')
        )
    get_listing_critics_with_admin_urls.short_description = _('Critics')

    def get_listing_supporters_with_admin_urls(self, obj):
        """ """

        return listing_objects_with_admin_url(
            obj.get_supporters(),
            'get_admin_url',
            'get_full_name',
            _('No body')
        )
    get_listing_supporters_with_admin_urls.short_description = _('Supporters')
