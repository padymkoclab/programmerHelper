
from django.utils.html import format_html_join, format_html
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.replies.admin import ReplyInline

from .models import Book, Writer
from .forms import BookForm, WriterForm
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
        'publishers',
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
        'language',
        'year_published',
        'date_added',
    )
    search_fields = ('name', 'publishers', 'users__name')
    date_hierarchy = 'date_added'

    # book
    form = BookForm
    filter_horizontal = ['tags']
    filter_vertical = ['authorship']
    radio_fields = {'language': admin.HORIZONTAL}
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = ['date_added', 'get_size_display', 'get_rating', 'show_most_common_words_from_replies']

    def get_queryset(self, request):

        qs = super(BookAdmin, self).get_queryset(request)
        qs = qs.books_with_count_tags_replies_and_rating()
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
                    'publishers',
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
        if rating < 3:
            color = 'red'
        elif 3 < rating < 4:
            color = 'black'
        elif rating > 4:
            color = 'green'

        return format_html('<span style="color: {0};">{1}<span>', color, rating)
    color_styled_rating.admin_order_field = 'rating'
    color_styled_rating.short_description = _('Rating')

    def show_most_common_words_from_replies(self, obj):
        return ', '.join(obj.get_most_common_words_from_replies())
    show_most_common_words_from_replies.short_description = _('Most common words from replies')


class WriterAdmin(admin.ModelAdmin):
    '''
    Admin View for Writer
    '''

    form = WriterForm
    list_display = (
        'name',
        'get_years_life',
        'get_age',
        'is_alive',
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
                    'books',
                ],
            }
        ]
    ]
    readonly_fields = ['get_count_books', 'get_age', 'get_years_life', 'is_alive', 'get_avg_mark_for_books', 'books']
    list_filter = [StatusLifeWriterSimpleListFilter, WritersCentriesSimpleListFilter]

    def get_queryset(self, request):
        qs = super(WriterAdmin, self).get_queryset(request)
        qs = qs.writers_with_count_books_and_avg_mark_by_rating_of_books()
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
                        'is_alive',
                        'get_avg_mark_for_books',
                        'books',
                    ],
                }
            ])

        return fieldsets
