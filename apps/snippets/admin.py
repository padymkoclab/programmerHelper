
# from django.template.defaultfilters import truncatechars
# from django.utils.translation import ugettext_lazy as _
# from django.contrib import admin

# from utils.django.listfilters import IsNewSimpleListFilter

from apps.admin.admin import ModelAdmin, TabularInline
from apps.admin.app import AppAdmin
from apps.admin.utils import register_app, register_model

# from apps.comments.admin import CommentGenericInline
# from apps.opinions.admin import OpinionGenericInline
from apps.opinions.admin_mixins import OpinionsAdminMixin

from .apps import SnippetsConfig
from .models import Snippet
from .forms import SnippetAdminModelForm


@register_app
class SnippetAppAdmin(AppAdmin):

    app_config_class = SnippetsConfig

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
                    (_('Count comments'), Snippet.comments_manager.get_count_comments()),
                    (_('Average count comments'), Snippet.comments_manager.get_avg_count_comments()),
                    (_('Count disticnt users posted comments'),
                        Snippet.comments_manager.get_count_distinct_users_posted_comments()),
                )
            ),
            (
                _('Opinions'), (
                    (_('Count opinions'), Snippet.opinions_manager.get_count_opinions()),
                    (_('Average count opinions'), Snippet.opinions_manager.get_avg_count_opinions()),
                    (_('Count critics'), Snippet.opinions_manager.get_count_critics()),
                    (_('Count supporters'), Snippet.opinions_manager.get_count_supporters()),
                )
            ),
            (
                _('Tags'), (
                    (_('Count used tags'), Snippet.tags_manager.get_count_used_tags()),
                    (_('Average count tags'), Snippet.tags_manager.get_avg_count_tags()),
                    (_('Count distinct used tags'), Snippet.tags_manager.get_count_distinct_used_tags()),
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


@register_model(Snippet)
class SnippetAdmin(OpinionsAdminMixin, ModelAdmin):
    '''
    Admin View for Snippet.
    '''

    form = SnippetAdminModelForm
    list_display = (
        'truncated_name',
        'user',
        'lexer',
        'get_rating',
        'get_count_tags',
        'get_count_opinions',
        'get_count_comments',
        'is_new',
        'updated',
        'created',
    )
    list_filter = (
        # ('user', admin.RelatedOnlyFieldListFilter),
        # ('lexer', admin.AllValuesFieldListFilter),
        # IsNewSimpleListFilter,
        # 'updated',
        # 'created',
    )

    search_fields = ('name', )
    filter_horizontal = ['tags']
    date_hierarchy = 'created'

    readonly_fields = [
        'get_rating',
        'get_count_tags',
        'get_count_opinions',
        'get_count_comments',
        'updated',
        'created',
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
                        'name',
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
                        'updated',
                        'created',
                    ],
                }
            ])

        return fieldsets

    def truncated_name(self, obj):
        return truncatechars(obj.name, 50)
    truncated_name.short_description = Snippet._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'

    def suit_row_attributes(self, obj, request):

        if obj.rating is not None:
            if obj.rating < 0:
                return {'class': 'error'}
            elif obj.rating > 0:
                return {'class': 'success'}

    def suit_cell_attributes(self, obj, column):

        css_text_align = 'center'
        if column in ['truncated_name']:
            css_text_align = 'left'
        elif column in ['updated', 'created']:
            css_text_align = 'right'
        else:
            css_text_align = 'center'

        return {'class': 'text-{}'.format(css_text_align)}

    def preview_snippet(self):
        """ """

        raise NotImplementedError
