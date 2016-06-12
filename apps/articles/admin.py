
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.scopes.admin import ScopeInline
from apps.comments.admin import CommentInline

from .forms import ArticleForm, ArticleSubsectionFormset
from .models import Article, ArticleSubsection


class ArticleSubsectionInline(admin.StackedInline):
    '''
    Tabular Inline View for Tag
    '''

    formset = ArticleSubsectionFormset
    model = ArticleSubsection
    min_num = Article.MIN_COUNT_SUBSECTIONS
    max_num = Article.MAX_COUNT_SUBSECTIONS
    fk_name = 'article'
    prepopulated_fields = {'slug': ['title']}
    fields = ['title', 'slug', 'content']
    extra = 0
    template = 'articles/stacked.html'


class ArticleAdmin(admin.ModelAdmin):
    '''
    Admin View for Article
    '''

    form = ArticleForm
    list_display = (
        'title',
        'account',
        'get_rating',
        'get_count_subsections',
        'get_count_links',
        'get_count_tags',
        'get_count_scopes',
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
    search_fields = ('title',)
    inlines = [
        ArticleSubsectionInline,
        ScopeInline,
        CommentInline,
    ]
    fieldsets = [
        (_('Basic info'), {
            'fields': [
                'title', 'slug', 'picture', 'account'
            ]
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
    readonly_fields = ['status_changed']
    prepopulated_fields = {'slug': ['title']}

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.articles_with_rating_and_count_comments_subsections_tags_links_scopes()
        return qs

    def get_count_links(self, obj):
        return obj.count_links
    get_count_links.admin_order_field = 'count_links'
    get_count_links.short_description = _('Count useful links')

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_scopes(self, obj):
        return obj.count_scopes
    get_count_scopes.admin_order_field = 'count_scopes'
    get_count_scopes.short_description = _('Count scopes')

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

    list_display = ('article', 'title', 'date_modified', 'date_added')
    list_filter = (
        ('article', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title', )
    date_hierarchy = 'date_modified'
    readonly_fields = ['slug']
    fieldsets = [
        [
            ArticleSubsection._meta.verbose_name, {
                'fields': ['article', 'title', 'slug', 'content'],
            }
        ]
    ]
