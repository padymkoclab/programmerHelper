
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Count

# from apps.generic_models.admin import OpinionGenericInline, CommentGenericInline

from .forms import SolutionForm
from .models import SolutionCategory, Solution


class SolutionInline(admin.StackedInline):
    '''
    Tabular Inline View for Solution
    '''

    model = Solution
    extra = 0
    fk_name = 'category'
    fields = ['title', 'body', 'tags', 'links']
    filter_vertical = ['links']
    filter_horizontal = ['tags']


class SolutionCategoryAdmin(admin.ModelAdmin):
    """
    Admin View for SolutionCategory
    """

    list_display = (
        'name',
        'lexer',
        'get_total_scope',
        'get_count_solutions',
        'is_new',
        'last_activity',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('lexer', admin.AllValuesFieldListFilter),
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    search_fields = ('name',)
    inlines = [
        SolutionInline,
    ]
    fieldsets = [
        [
            SolutionCategory._meta.verbose_name, {
                'fields': ['name', 'lexer', 'description']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(SolutionCategoryAdmin, self).get_queryset(request)
        qs = qs.annotate(count_solutions=Count('solutions'))
        return qs

    def get_count_solutions(self, obj):
        return obj.count_solutions
    get_count_solutions.short_description = _('Count solutions')
    get_count_solutions.admin_order_field = 'count_solutions'


class SolutionAdmin(admin.ModelAdmin):
    """
    Admin View for Solution
    """

    list_display = (
        'title',
        'category',
        'get_scope',
        'account',
        'get_count_links',
        'get_count_opinions',
        'get_count_comments',
        'get_count_tags',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
        ('account', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title',)
    date_hierarchy = 'date_added'
    inlines = [
        # OpinionGenericInline,
        # CommentGenericInline,
    ]
    fieldsets = [
        [
            Solution._meta.verbose_name, {
                'fields': ['title', 'category', 'body', 'tags', 'links'],
            }
        ],
    ]

    filter_horizontal = ['tags']
    filter_vertical = ['links']
    form = SolutionForm

    def get_queryset(self, request):
        qs = super(SolutionAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_links=Count('links', distinct=True),
            count_opinions=Count('opinions', distinct=True),
            count_comments=Count('comments', distinct=True),
            count_tags=Count('tags', distinct=True),
        )
        return qs

    def get_count_links(self, obj):
        return obj.count_links
    get_count_links.short_description = _('Count links')
    get_count_links.admin_order_field = 'count_links'

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.short_description = _('Count opinions')
    get_count_opinions.admin_order_field = 'count_opinions'

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.short_description = _('Count comments')
    get_count_comments.admin_order_field = 'count_comments'

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')
