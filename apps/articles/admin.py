
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.marks.admin import MarkGenericInline
from apps.comments.admin import CommentGenericInline

from apps.admin.admin import ModelAdmin
from apps.admin.app import AppAdmin
from apps.admin.site import DefaultSiteAdmin

from .forms import ArticleAdminModelForm, SubsectionAdminModelForm
from .formsets import SubsectionFormset
from .models import Article, Subsection
from .apps import ArticlesConfig
from .actions import make_articles_as_draft, make_articles_as_published


class ArticlesAppAdmin(AppAdmin):

    app_config_class = ArticlesConfig
    app_icon = 'users'

    def get_context_for_tables_of_statistics(self):

        return (
            (_('Articles'), (
                (_('Count articles'), Article.objects.count()),
                (_('Count subsections'), Subsection.objects.count()),
                (_('Average count subsections'), Article.objects.get_avg_count_subsections()),
            )),
            (_('Tags'), (
                (_('Count used tags'), Article.tags_manager.get_count_used_tags()),
                (_('Count distinct used tags'), Article.tags_manager.get_count_distinct_used_tags()),
                (_('Average count tags'), Article.tags_manager.get_avg_count_tags()),
            )),
            (_('Comments'), (
                (_('Count comments'), Article.comments_manager.get_count_comments()),
                (_('Average count comments'), Article.comments_manager.get_avg_count_comments()),
            )),
            (_('Marks'), (
                (_('Total count marks'), Article.marks_manager.get_total_count_marks()),
                (_('Average count marks on article'), Article.marks_manager.get_avg_count_marks_on_object()),
            )),
        )

    def get_context_for_charts_of_statistics(self):

        return (
            {
                'title': _('Chart count articles for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count articles')),
                    'data': Article.objects.get_statistics_count_articles_for_the_past_year(),
                },
                'chart': Article.objects.get_chart_count_articles_for_the_past_year(),
            },
            {
                'title': _('Chart count comments for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count comments')),
                    'data': Article.comments_manager.get_statistics_count_comments_for_the_past_year(),
                },
                'chart': Article.comments_manager.get_chart_count_comments_for_the_past_year(),
            },
            {
                'title': _('Chart used marks'),
                'table': {
                    'fields': (_('Mark'), _('Count used')),
                    'data': Article.marks_manager.get_statistics_used_marks(),
                },
                'chart': Article.marks_manager.get_chart_used_marks(),
            },
            {
                'title': _('Chart most used tags'),
                'table': None,
                'chart': Article.tags_manager.get_chart_most_used_tags(),
            },
        )


class SubsectionInline(admin.StackedInline):
    '''
    Tabular Inline View for Tag
    '''

    form = SubsectionAdminModelForm
    formset = SubsectionFormset
    model = Subsection
    min_num = 1
    max_num = Article.MAX_COUNT_SUBSECTIONS
    fk_name = 'article'
    prepopulated_fields = {'slug': ['name']}
    extra = 0
    fieldsets = (
        (
            None, {
                'fields': ('name', 'slug',)
            }
        ),
        (
            None, {
                'classes': ('full-width', ),
                'fields': ('content', ),
            }
        ),
    )

    suit_classes = 'suit-tab suit-tab-subsections'


class ArticleAdmin(ModelAdmin):
    '''
    Admin View for Article
    '''

    # formfield_overrides =
    suit_form_tabs = (
        ('general', _('General')),
        ('header', _('Header')),
        ('subsections', _('Subsections')),
        ('footer', _('Footer')),
        ('marks', _('Marks')),
        ('comments', _('Comments')),
        ('statistics', _('Statistics')),
    )

    form = ArticleAdminModelForm
    list_display = (
        'truncated_name',
        'user',
        'status',
        'get_rating',
        'get_count_subsections',
        'get_count_links',
        'get_count_tags',
        'get_count_marks',
        'get_count_comments',
        'is_new',
        'updated',
        'created',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'status',
        'updated',
        'created',
    )
    search_fields = ('name',)
    filter_horizontal = ['tags']
    date_hierarchy = 'created'
    prepopulated_fields = {'slug': ['name']}
    readonly_fields = (
        'get_rating',
        'get_volume',
        'get_count_marks',
        'get_count_subsections',
        'get_count_links',
        'get_count_tags',
        'get_related_objects',
        'get_count_comments',
    )
    actions = [make_articles_as_draft, make_articles_as_published]

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.articles_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                None, {
                    'classes': ('suit-tab', 'suit-tab-general',),
                    'fields': [
                        'name',
                        'slug',
                        'user',
                        'status',
                        'image',
                        'links',
                        'tags',
                    ],
                }
            ),
            (
                Article._meta.get_field('quotation').verbose_name, {
                    'classes': ('suit-tab', 'suit-tab-header'),
                    'fields': ('quotation', ),
                }
            ),
            (
                Article._meta.get_field('heading').verbose_name, {
                    'classes': ('full-width', 'suit-tab', 'suit-tab-header'),
                    'fields': ('heading', ),
                }
            ),
            (
                Article._meta.get_field('conclusion').verbose_name, {
                    'classes': ('full-width', 'suit-tab', 'suit-tab-footer'),
                    'fields': ('conclusion', ),
                }
            ),
        ]

        if obj is not None:
            fieldsets.append(
                (
                    _('Statistics'), {
                        'classes': ('suit-tab', 'suit-tab-statistics'),
                        'fields': {
                            'get_rating',
                            'get_volume',
                            'get_count_marks',
                            'get_count_subsections',
                            'get_count_links',
                            'get_count_tags',
                            'get_related_objects',
                            'get_count_comments',
                        }
                    }
                ),
            )

        return fieldsets

    def get_inline_instances(self, reuest, obj=None):

        if obj is not None:
            inlines = [SubsectionInline, MarkGenericInline, CommentGenericInline]
            return [inline(self.model, self.admin_site) for inline in inlines]

        return []

    def truncated_name(self, obj):

        return truncatechars(obj.name, 75)
    truncated_name.short_description = Article._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'


DefaultSiteAdmin.register_app(ArticlesAppAdmin)
DefaultSiteAdmin.register_model(Article, ArticleAdmin)
