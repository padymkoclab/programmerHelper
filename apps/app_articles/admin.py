
from django.db.models import Count, Avg
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.app_generic_models.admin import ScopeGenericInline, CommentGenericInline

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
        'author',
        'get_count_subsections',
        'get_count_useful_links',
        'get_count_tags',
        'get_rating',
        'get_rating_admin',
        'get_count_comments',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title', 'web_url')
    inlines = [
        ScopeGenericInline,
        ArticleSubsectionInline,
        CommentGenericInline,
    ]
    fieldsets = [
        (_('Basic'), {
            'fields': ['title', 'picture', 'author']
        }),
        (_('Status'), {
            'fields': ['status', 'status_changed']
        }),
        (_('Header'), {
            'fields': ['quotation', 'header']
        }),
        # (_('Content'), {
        #     'fields': ['quotation', 'header', 'conclusion']
        # }),
        (_('Footer'), {
            'fields': ['conclusion', 'useful_links', 'tags']
        }),
    ]
    filter_horizontal = ['tags']
    filter_vertical = ['useful_links']
    date_hierarchy = 'date_added'

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_tags=Count('tags', distinct=True),
            count_useful_links=Count('useful_links', distinct=True),
            count_subsections=Count('subsections', distinct=True),
            count_comments=Count('comments', distinct=True),
        )
        return qs

    def get_count_useful_links(self, obj):
        return obj.count_useful_links
    get_count_useful_links.admin_order_field = 'count_useful_links'
    get_count_useful_links.short_description = _('Count useful links')

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

    def get_rating_admin(self, obj):
        avg_scope = obj.scopes.aggregate(rating=Avg('scope'))['rating'] or float(0)
        return float('{0:.3}'.format(avg_scope))
        # return obj.get_rating()
    get_rating_admin.short_description = _('Rating')
    get_rating_admin.admin_order_field = 'scopes__rating'


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
    search_fields = ('title', 'article__title')
    date_hierarchy = 'date_modified'
    fields = ['article', 'title', 'content']
