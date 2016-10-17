
from django.utils.html import format_html_join
from django.utils.encoding import force_str
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.listfilters import AllValuesChoicesFieldListFilter

# from apps.core.admin import AdminSite, AppAdmin
from apps.replies.admin import ReplyGenericInline

from .models import Book, Writer, Publisher
from .forms import BookAdminModelForm, WriterAdminModelForm, PublisherAdminModelForm
from .listfilters import (
    BookSizeSimpleListFilter,
    StatusLifeWriterSimpleListFilter,
    WritersCentriesSimpleListFilter
)
from .apps import LibraryConfig


# @AdminSite.register_app_admin_class
# class ThisAppAdmin(AppAdmin):
class ThisAppAdmin():

    label = LibraryConfig.label

    def get_context_for_tables_of_statistics(self):

        return (
            (_('Books'), (
                (_('Count books'), Book.objects.count()),
                (_('Count russian books'), Book.objects.get_count_russian_books()),
                (_('Count english books'), Book.objects.get_count_english_books()),
                (_('Count great books'), Book.objects.get_count_great_books()),
                (_('Count big books'), Book.objects.get_count_big_books()),
                (_('Count middle books'), Book.objects.get_count_middle_books()),
                (_('Count tiny books'), Book.objects.get_count_tiny_books()),
            )),
            (_('Writers'), (
                (_('Count writers'), Writer.objects.count()),
                (_('Average count books on writer'), Writer.objects.get_avg_count_books()),
            )),
            (_('Publishers'), (
                (_('Count publishers'), Publisher.objects.count()),
                (_('Average count books on publishers'), Publisher.objects.get_avg_count_books()),
            )),
            (_('Replies'), (
                (_('Count replies'), Book.replies_manager.get_count_replies()),
                (_('Average count replies on book'), Book.replies_manager.get_avg_count_replies()),
            )),
            (_('Tags'), (
                (_('Count used tags'), Book.tags_manager.get_count_used_tags()),
                (_('Count distinct tags'), Book.tags_manager.get_count_distinct_used_tags()),
                (_('Average count tags on book'), Book.tags_manager.get_avg_count_tags()),
            )),
        )

    def get_context_for_charts_of_statistics(self):

        return (
            {
                'title': _('Chart count books by size'),
                'table': None,
                'chart': Book.objects.get_chart_statistics_count_books_by_size(),
            },
            {
                'title': _('Chart count replies for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count replies')),
                    'data': Book.replies_manager.get_statistics_count_replies_for_the_past_year(),
                },
                'chart': Book.replies_manager.get_chart_count_replies_for_the_past_year(),
            },
        )


# @admin.register(Book, site=AdminSite)
class BookAdmin(admin.ModelAdmin):
    '''
    Admin View for Book
    '''

    list_display = (
        'name',
        'show_authorship_inline',
        'publisher',
        'language',
        'count_pages',
        'get_size_display',
        'get_count_tags',
        'get_count_replies',
        'get_rating',
        'is_new',
        'year_published',
        'created',
    )
    list_filter = (
        BookSizeSimpleListFilter,
        ('publisher', admin.RelatedOnlyFieldListFilter),
        ('authorship', admin.RelatedOnlyFieldListFilter),
        'language',
        'year_published',
        'created',
    )
    search_fields = ('name', )
    date_hierarchy = 'created'

    form = BookAdminModelForm
    filter_horizontal = ['tags']
    filter_vertical = ['authorship']
    radio_fields = {'language': admin.HORIZONTAL}
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = [
        'created',
        'get_size_display',
        'get_count_replies',
        'get_rating',
        'get_most_common_words_from_replies'
    ]

    list_select_related = True

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        qs = qs.books_with_additional_fields()
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = (ReplyGenericInline, )
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def get_fieldsets(self, request, obj=None):
        fieldsets = [[
            Book._meta.verbose_name, {
                'fields': [
                    'name',
                    'slug',
                    'description',
                    'image',
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

        if obj is not None:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'created',
                        'get_size_display',
                        'get_count_replies',
                        'get_rating',
                        'get_most_common_words_from_replies',
                    ]
                }
            ])

        return fieldsets

    def suit_cell_attributes(self, obj, column):

        if column == 'name':
            class_css = 'left'
        elif column == 'created':
            class_css = 'right'
        else:
            class_css = 'center'

        return {'class': 'text-{}'.format(class_css)}

    def suit_row_attributes(self, obj, request):

        rating = obj.get_rating()

        class_css = 'default'

        if rating is not None:
            if 4 <= rating <= 5:
                class_css = 'success'
            elif rating < 2:
                class_css = 'error'

        return {'class': '{}'.format(class_css)}

    def show_authorship_inline(self, obj):

        authorship = map(force_str, obj.authorship.iterator())
        return format_html_join(', ', '{}<br />', ((writer, ) for writer in authorship))
    show_authorship_inline.short_description = Book._meta.get_field('authorship').verbose_name

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

    def suit_cell_attributes(self, obj, column):
        """ """

        raise Exception()
        if column == 'countries':
            return {'class': 'text-center'}
        elif column == 'name' and obj.status == -1:
            return {'class': 'text-error'}

        if column == 'rating':
            class_css = 'right'
        elif column == 'count_replies':
            class_css = 'center'
        else:
            class_css = 'left'

        return {'class': 'text-{}'.format(class_css)}


class BookInlineForPublisher(admin.TabularInline):
    """Readonly inline of books for each publisher."""

    model = Book
    can_delete = False
    fields = ['name', 'get_count_replies', 'get_rating']
    readonly_fields = ['name', 'get_count_replies', 'get_rating']
    max_num = 0


# @admin.register(Writer, site=AdminSite)
class WriterAdmin(admin.ModelAdmin):
    '''
    Admin View for Writer
    '''

    form = WriterAdminModelForm
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
        qs = super().get_queryset(request)
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
            inlines = [BookInlineForWriter]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def suit_cell_attributes(self, obj, column):

        if column == 'get_avg_mark_for_books':
            class_css = 'right'
        elif column in ['name', 'get_years_life']:
            class_css = 'left'
        else:
            class_css = 'center'

        return {'class': 'text-{}'.format(class_css)}

    def suit_row_attributes(self, obj, request):

        avg_mark_for_books = obj.get_avg_mark_for_books()

        css_class = 'default'
        if avg_mark_for_books is not None:
            if 4 <= obj.get_avg_mark_for_books() <= 5:
                css_class = 'success'
            elif obj.get_avg_mark_for_books() < 2:
                css_class = 'error'

        return {'class': '{}'.format(css_class)}


# @admin.register(Publisher, site=AdminSite)
class PublisherAdmin(admin.ModelAdmin):

    form = PublisherAdminModelForm
    search_fields = ('name', )
    list_display = (
        'name',
        'get_count_books',
        'country_origin',
        'headquarters',
        'founded_year',
        'website',
    )
    readonly_fields = ('get_count_books', )
    list_filter = (
        ('country_origin', AllValuesChoicesFieldListFilter),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.publishers_with_count_books()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = (
            (
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
            ),
        )

        if obj is not None:

            fieldsets[0][1]['fields'].insert(3, 'get_count_books')

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj and obj.books.exists():
            inlines = [BookInlineForPublisher]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def suit_cell_attributes(self, obj, column):

        if column in ['founded_year', 'get_count_books']:
            css_class = 'center'
        else:
            css_class = 'left'

        return {'class': 'text-{}'.format(css_class)}
