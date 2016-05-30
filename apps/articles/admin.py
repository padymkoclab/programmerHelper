
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# from apps.generic_models.admin import ScopeGenericInline, CommentGenericInline

from .forms import ArticleForm
from .models import Article, ArticleSubsection


class ArticleSubsectionInline(admin.StackedInline):
    '''
    Tabular Inline View for Tag
    '''

    model = ArticleSubsection
    min_num = Article.MIN_COUNT_SUBSECTIONS
    max_num = Article.MAX_COUNT_SUBSECTIONS
    fk_name = 'article'
    fields = ['title', 'content']
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    '''
    Admin View for Article
    '''

    form = ArticleForm
    list_display = (
        'title',
        'picture',
        'account',
        'get_rating',
        'get_count_subsections',
        'get_count_links',
        'get_count_tags',
        'get_count_comments',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title', 'web_url')
    inlines = [
        # ScopeGenericInline,
        ArticleSubsectionInline,
        # CommentGenericInline,
    ]
    fieldsets = [
        (_('Basic'), {
            'fields': ['title', 'picture', 'account']
        }),
        (_('Status'), {
            'fields': ['status', 'status_changed']
        }),
        (_('Header'), {
            'fields': ['quotation', 'header']
        }),
        (_('Footer'), {
            'fields': ['conclusion', 'links', 'tags']
        }),
    ]
    filter_horizontal = ['tags']
    filter_vertical = ['links']
    date_hierarchy = 'date_added'

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_tags=models.Count('tags', distinct=True),
            count_links=models.Count('links', distinct=True),
            count_subsections=models.Count('subsections', distinct=True),
            count_comments=models.Count('comments', distinct=True),
            rating=models.Avg('scopes__scope', distinct=True),
        )
        return qs

    def get_count_links(self, obj):
        return obj.count_links
    get_count_links.admin_order_field = 'count_links'
    get_count_links.short_description = _('Count useful links')

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_subsections(self, obj):
        return obj.count_subsections
    get_count_subsections.admin_order_field = 'count_subsections'
    get_count_subsections.short_description = _('Count subsections')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')


class ArticleSubsectionAdmin(admin.ModelAdmin):
    '''
        Admin View for ArticleSubsection
    '''

    list_display = ('title', 'article', 'date_modified', 'date_added')
    list_filter = (
        ('article', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title', )
    date_hierarchy = 'date_modified'
    fieldsets = [
        [
            ArticleSubsection._meta.verbose_name, {
                'fields': ['article', 'title', 'content'],
            }
        ]
    ]
