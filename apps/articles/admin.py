
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.core.admin import AdminSite, AppAdmin
from apps.marks.admin import MarkGenericInline
from apps.comments.admin import CommentGenericInline

from .forms import ArticleAdminModelForm, SubsectionAdminModelForm
from .formsets import SubsectionFormset
from .models import Article, Subsection


class SubsectionInline(admin.StackedInline):
    '''
    Tabular Inline View for Tag
    '''

    form = SubsectionAdminModelForm
    formset = SubsectionFormset
    model = Subsection
    min_num = 1
    max_num = Article.MAX_COUNT_SUBSECTIONS
    fk_name = 'article'
    prepopulated_fields = {'slug': ['title']}
    extra = 0
    fieldsets = (
        (
            None, {
                'fields': ('title', 'slug',)
            }
        ),
        (
            None, {
                'classes': ('full-width', ),
                'fields': ('content', ),
            }
        ),
    )

    suit_classes = 'suit-tab suit-tab-subsections'


@admin.register(Article, site=AdminSite)
class ArticleAdmin(admin.ModelAdmin):
    '''
    Admin View for Article
    '''

    # formfield_overrides =
    suit_form_tabs = (
        ('general', _('General')),
        ('header', _('Header')),
        ('subsections', _('Subsections')),
        ('footer', _('Footer')),
        ('marks', _('Marks')),
        ('comments', _('Comments')),
        ('statistics', _('Statistics')),
    )

    form = ArticleAdminModelForm
    list_display = (
        'truncated_title',
        'user',
        'get_rating',
        'get_count_subsections',
        'get_count_links',
        'get_count_tags',
        'get_count_marks',
        'get_count_comments',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title',)
    filter_horizontal = ['tags']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = (
        'get_rating',
        'get_volume',
        'get_count_marks',
        'get_count_subsections',
        'get_count_links',
        'get_count_tags',
        'get_related_objects',
        'get_count_comments',
    )

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        qs = qs.articles_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                None, {
                    'classes': ('suit-tab', 'suit-tab-general',),
                    'fields': [
                        'title',
                        'slug',
                        'user',
                        'status',
                        'image',
                        'links',
                        'tags',
                    ],
                }
            ),
            (
                Article._meta.get_field('quotation').verbose_name, {
                    'classes': ('suit-tab', 'suit-tab-header'),
                    'fields': ('quotation', ),
                }
            ),
            (
                Article._meta.get_field('heading').verbose_name, {
                    'classes': ('full-width', 'suit-tab', 'suit-tab-header'),
                    'fields': ('heading', ),
                }
            ),
            (
                Article._meta.get_field('conclusion').verbose_name, {
                    'classes': ('full-width', 'suit-tab', 'suit-tab-footer'),
                    'fields': ('conclusion', ),
                }
            ),
        ]

        if obj is not None:
            fieldsets.append(
                (
                    _('Statistics'), {
                        'classes': ('suit-tab', 'suit-tab-statistics'),
                        'fields': {
                            'get_rating',
                            'get_volume',
                            'get_count_marks',
                            'get_count_subsections',
                            'get_count_links',
                            'get_count_tags',
                            'get_related_objects',
                            'get_count_comments',
                        }
                    }
                ),
            )

        return fieldsets

    def get_inline_instances(self, reuest, obj=None):

        if obj is not None:
            inlines = [SubsectionInline, MarkGenericInline, CommentGenericInline]
            return [inline(self.model, self.admin_site) for inline in inlines]

        return []

    def suit_row_attributes(self, obj, request):

        css_class = 'default'
        if obj.rating is not None:
            if 4 <= obj.rating <= 5:
                css_class = 'success'
            if obj.rating < 2:
                css_class = 'error'

        return {'class': css_class}

    def suit_cell_attributes(self, obj, column):

        if column in ['date_added', 'date_modified']:
            css_class = 'right'
        elif column == 'title':
            css_class = 'left'
        else:
            css_class = 'center'

        return {'class': 'text-{}'.format(css_class)}

    def truncated_title(self, obj):

        return truncatechars(obj.title, 75)
    truncated_title.short_description = Article._meta.get_field('title').verbose_name
    truncated_title.admin_order_field = 'title'
