
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.app_generic_models.admin import OpinionGenericInline, CommentGenericInline


class BookAdmin(admin.ModelAdmin):
    '''
    Admin View for Book
    '''

    list_display = (
        'name',
        'pages',
        'views',
        'publishers',
        'isbn',
        'get_count_links_where_download',
        'get_count_tags',
        'get_count_opinions',
        'get_count_comments',
        'date_published',
    )
    list_filter = ('date_published',)
    inlines = [
        OpinionGenericInline,
        CommentGenericInline,
    ]
    search_fields = ('name', 'publishers')
    date_hierarchy = 'date_published'
    filter_horizontal = ['tags', 'authorship']
    filter_vertical = ['where_download']
    fields = [
        'name',
        'description',
        'picture',
        'pages',
        'date_published',
        'isbn',
        'publishers',
        'authorship',
        'where_download',
        'tags',
    ]

    def get_queryset(self, request):
        qs = super(BookAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_comments=Count('comments', distinct=True),
            count_tags=Count('tags', distinct=True),
            count_links_where_download=Count('where_download', distinct=True),
            count_opinions=Count('opinions', distinct=True),
        )
        return qs

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def get_count_links_where_download(self, obj):
        return obj.count_links_where_download
    get_count_links_where_download.admin_order_field = 'count_links_where_download'
    get_count_links_where_download.short_description = _('Count links where download')


class WritterAdmin(admin.ModelAdmin):
    '''
        Admin View for Writter
    '''
    list_display = ('name', 'short_about')
    search_fields = ['name', 'about']
    fields = ['name', 'about']
