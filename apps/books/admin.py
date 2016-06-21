
from django.utils.html import format_html_join
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.replies.admin import ReplyInline

from .models import Book, Writter
from .forms import BookForm, WritterForm


class BookAdmin(admin.ModelAdmin):
    '''
    Admin View for Book
    '''

    form = BookForm
    list_display = (
        'name',
        'show_writters',
        'pages',
        'publishers',
        'language',
        'isbn',
        'get_count_tags',
        'get_rating',
        'get_count_replies',
        'is_new',
        'get_size',
        'year_published',
    )
    list_filter = ('year_published', 'language')
    inlines = [
        ReplyInline,
    ]
    search_fields = ('name', 'publishers', 'accounts__name')
    date_hierarchy = 'date_added'
    filter_horizontal = ['tags']
    filter_vertical = ['accounts']
    fieldsets = [
        [
            Book._meta.verbose_name, {
                'fields': [
                    'name',
                    'description',
                    'picture',
                    'pages',
                    'year_published',
                    'language',
                    'isbn',
                    'publishers',
                    'accounts',
                    'tags',
                ]
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(BookAdmin, self).get_queryset(request)
        qs = qs.books_with_count_tags_links_replies_and_rating()
        return qs

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_replies(self, obj):
        return obj.count_replies
    get_count_replies.admin_order_field = 'count_replies'
    get_count_replies.short_description = _('Count replies')

    def show_writters(self, obj):
        """Listing writters separated throgh commas"""

        return format_html_join(', ', '{0}', ((writter, ) for writter in obj.accounts.all()))
    show_writters.short_description = _('Writters')

    def color_styled_rating(self, obj):
        raise NotImplementedError


class WritterAdmin(admin.ModelAdmin):
    '''
    Admin View for Writter
    '''

    form = WritterForm
    list_display = (
        'name',
        'show_years_life',
        'show_books',
        'get_count_books',
        'short_about_writter',
    )
    search_fields = ['name', 'about']
    fieldsets = [
        [
            Writter._meta.verbose_name, {
                'fields': [
                    'name',
                    'about',
                    'years_life',
                ],
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(WritterAdmin, self).get_queryset(request)
        qs = qs.writters_with_count_books()
        return qs

    def get_count_books(self, obj):
        return obj.count_books
    get_count_books.admin_order_field = 'count_books'
    get_count_books.short_description = _('Count books')

    def show_books(self, obj):
        return format_html_join(', ', '"{0}"', ((book, ) for book in obj.books.all()))
    show_books.admin_order_field = 'count_books'
    show_books.short_description = _('Books')

    def short_about_writter(self, obj):
        return truncatewords(obj.about, 10)
    short_about_writter.short_description = _('Short about writter')
