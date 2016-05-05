
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .forms import ArticleForm
from .models import Article, ArticleSubsection, ArticleComment


class OpinionAboutArticleInline(admin.TabularInline):
    '''
        Tabular Inline View for Tag
    '''

    model = Article.opinions.through
    extra = 1
    fields = ['user', 'is_useful', 'is_favorite']
    # verbose_name = _('Opinion')
    # verbose_name_plural = _('Voted users')


class ArticleSubsectionInline(admin.StackedInline):
    '''
    Tabular Inline View for Tag
    '''

    model = ArticleSubsection
    min_num = Article.MIN_COUNT_SUBSECTIONS
    max_num = Article.MAX_COUNT_SUBSECTIONS
    fk_name = 'article'
    fields = ['title', 'content']
    extra = 1


class ArticleCommentInline(admin.StackedInline):
    '''
    Tabular Inline View for Tag
    '''

    model = ArticleComment
    fk_name = 'article'
    fields = ['article', 'author', 'text_comment']
    extra = 1
    verbose_name = _('Comment')


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
        'get_count_opinions',
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
        ArticleSubsectionInline,
        OpinionAboutArticleInline,
        ArticleCommentInline,
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
            count_opinions=Count('opinions', distinct=True),
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

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_subsections(self, obj):
        return obj.count_subsections
    get_count_subsections.admin_order_field = 'count_subsections'
    get_count_subsections.short_description = _('Count subsections')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')


class OpinionAboutArticleAdmin(admin.ModelAdmin):
    '''
        Admin View for OpinionAboutArticle
    '''

    list_display = ('user', 'article', 'is_useful', 'display_is_favorite_as_boolean', 'date_modified')
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('article', admin.RelatedOnlyFieldListFilter),
        ('is_useful', admin.BooleanFieldListFilter),
        'is_favorite',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    fields = ['article', 'user', 'is_useful', 'is_favorite']


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


class ArticleCommentAdmin(admin.ModelAdmin):
    '''
        Admin View for ArticleComment
    '''
    list_display = ('article', 'author', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('article', admin.RelatedOnlyFieldListFilter),
        ('author', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_modified'
    fields = ['article', 'author', 'text_comment']
