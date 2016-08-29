
from django.utils.html import format_html_join, format_html
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.replies.admin import ReplyInline

from .models import Book, Writer, Publisher
from .forms import BookForm, WriterForm, PublisherForm
from .listfilters import (
    BookSizeSimpleListFilter,
    StatusLifeWriterSimpleListFilter,
    WritersCentriesSimpleListFilter
)


class BookAdmin(admin.ModelAdmin):
    '''
    Admin View for Book
    '''

    # changelist
    list_display = (
        'name',
        'count_pages',
        'get_size_display',
        'publisher',
        'language',
        'get_count_tags',
        'get_count_replies',
        'color_styled_rating',
        'is_new',
        'year_published',
        'date_added',
    )
    list_filter = (
        BookSizeSimpleListFilter,
        ('publisher', admin.RelatedOnlyFieldListFilter),
        'language',
        'year_published',
        'date_added',
    )
    search_fields = ('name', )
    date_hierarchy = 'date_added'

    # book
    form = BookForm
    filter_horizontal = ['tags']
    filter_vertical = ['authorship']
    radio_fields = {'language': admin.HORIZONTAL}
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = ['date_added', 'get_size_display', 'get_rating', 'show_most_common_words_from_replies']

    list_select_related = True

    def get_queryset(self, request):

        qs = super(BookAdmin, self).get_queryset(request)
        qs = qs.books_with_additional_fields()
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = (ReplyInline, )
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def get_fieldsets(self, request, obj=None):
        fieldsets = [[
            Book._meta.verbose_name, {
                'fields': [
                    'name',
                    'slug',
                    'description',
                    'picture',
                    'count_pages',
                    'year_published',
                    'language',
                    'isbn',
                    'publisher',
                    'authorship',
                    'tags',
                ]
            },
        ]]

        # if book exists
        if obj:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'date_added',
                        'get_size_display',
                        'get_rating',
                        'show_most_common_words_from_replies',
                    ]
                }
            ])

        return fieldsets

    def color_styled_rating(self, obj):
        """Return colored value of rating for each book."""

        rating = obj.get_rating()
        color = None

        if rating is not None:
            if rating < 3:
                color = 'red'
            elif rating > 4:
                color = 'green'

        if color is not None:
            return format_html('<span style="color: {0};">{1}<span>', color, rating)

        return rating
    color_styled_rating.admin_order_field = 'rating'
    color_styled_rating.short_description = _('Rating')

    def show_most_common_words_from_replies(self, obj):
        return ', '.join(obj.get_most_common_words_from_replies())
    show_most_common_words_from_replies.short_description = _('Most common words from replies')


class BookInlineForWriter(admin.TabularInline):
    """Readonly inline of books for each writer."""

    model = Writer.books.through
    can_delete = False
    fields = ['book', 'get_count_replies', 'get_rating']
    readonly_fields = ['book', 'get_count_replies', 'get_rating']
    max_num = 0

    def __init__(self, *args, **kwargs):
        self.model._meta.verbose_name_plural = _('Books')
        super(BookInlineForWriter, self).__init__(*args, **kwargs)

    def get_rating(self, obj):
        """Access to a book`s method """

        return obj.book.get_rating()
    get_rating.short_description = _('Rating')

    def get_count_replies(self, obj):
        """Access to a book`s method """

        return obj.book.get_count_replies()
    get_count_replies.short_description = _('Count replies')


class BookInlineForPublisher(admin.TabularInline):
    """Readonly inline of books for each publisher."""

    model = Book
    can_delete = False
    fields = ['name', 'get_count_replies', 'get_rating']
    readonly_fields = ['name', 'get_count_replies', 'get_rating']
    max_num = 0


class WriterAdmin(admin.ModelAdmin):
    '''
    Admin View for Writer
    '''

    form = WriterForm
    list_display = (
        'name',
        'get_years_life',
        'get_age',
        'is_alive_writer',
        'get_count_books',
        'get_avg_mark_for_books',
    )
    search_fields = ['name', 'about']
    fieldsets = [
        [
            Writer._meta.verbose_name, {
                'fields': [
                    'name',
                    'slug',
                    'about',
                    'trends',
                    ('birth_year', 'death_year'),
                ],
            }
        ]
    ]
    readonly_fields = ['get_count_books', 'get_age', 'get_years_life', 'is_alive_writer', 'get_avg_mark_for_books']
    list_filter = [StatusLifeWriterSimpleListFilter, WritersCentriesSimpleListFilter]

    def get_queryset(self, request):
        qs = super(WriterAdmin, self).get_queryset(request)
        qs = qs.writers_with_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Writer._meta.verbose_name, {
                    'fields': [
                        'name',
                        'slug',
                        'about',
                        'trends',
                        ('birth_year', 'death_year'),
                    ],
                }
            ]
        ]

        if obj:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_count_books',
                        'get_age',
                        'get_years_life',
                        'is_alive_writer',
                        'get_avg_mark_for_books',
                    ],
                }
            ])

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj and obj.books.exists():
            # readonly inline if writer has books
            inlines = [BookInlineForWriter]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []


class PublisherAdmin(admin.ModelAdmin):

    form = PublisherForm
    search_fields = ['name']
    list_display = ['name', 'get_count_books', 'country_origin', 'headquarters', 'founded_year', 'website']
    readonly_fields = ['get_count_books']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.publishers_with_count_books()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Publisher._meta.verbose_name, {
                    'fields': [
                        'name',
                        'slug',
                        'country_origin',
                        'headquarters',
                        'founded_year',
                        'website',
                    ]
                }
            ]
        ]

        if obj is not None:

            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': {
                        'get_count_books',
                    }
                }
            ])

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj and obj.books.exists():
            inlines = [BookInlineForPublisher]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []
