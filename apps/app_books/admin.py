
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import BookComment, OpinionAboutBook


class BookCommentInline(admin.StackedInline):
    '''
        Stacked Inline View for BookComment
    '''
    model = BookComment
    extra = 1
    fk_name = 'book'
    fields = ['book', 'author', 'content']


class OpinionAboutBookInline(admin.TabularInline):
    '''
    Tabular Inline View for OpinionAboutBook
    '''
    model = OpinionAboutBook
    extra = 1


class BookAdmin(admin.ModelAdmin):
    '''
    Admin View for Book
    '''

    list_display = ('name', 'pages', 'views', 'publishers', 'isbn', 'date_published')
    list_filter = ('date_published',)
    inlines = [
        BookCommentInline,
        OpinionAboutBookInline,
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
            count_comments=Count('comments'),
            count_tags=Count('tags'),
            count_links_where_download=Count('where_download'),
            count_opinions=Count('opinions'),
        )

    def get_count_op(self):
        pass
