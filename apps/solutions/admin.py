
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.html import format_html

from mylabour.admin_listfilters import LatestActivityListFilter
# from apps.generic_models.admin import OpinionGenericInline, CommentGenericInline

from .forms import SolutionCategoryForm, SolutionForm
from .models import SolutionCategory, Solution


class SolutionCategoryAdmin(admin.ModelAdmin):
    """
    Admin View for SolutionCategory
    """

    list_display = (
        'name',
        'get_total_scope',
        'get_count_solutions',
        'get_latest_activity',
        'date_modified',
        'date_added',
    )
    list_filter = (
        LatestActivityListFilter,
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    search_fields = ('name',)
    fieldsets = [
        [
            SolutionCategory._meta.verbose_name, {
                'fields': ['name', 'slug', 'description']
            }
        ]
    ]
    form = SolutionCategoryForm

    def get_queryset(self, request):
        qs = super(SolutionCategoryAdmin, self).get_queryset(request)
        qs = qs.categories_with_count_solutions_total_scope_and_latest_activity()
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
        'colored_quality',
        'account',
        # 'get_count_links',
        # 'get_count_opinions',
        # 'get_count_comments',
        # 'get_count_tags',
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
                'fields': ['title', 'slug', 'category', 'account', 'body', 'tags', 'links'],
            }
        ],
    ]

    filter_horizontal = ['tags']
    filter_vertical = ['links']
    form = SolutionForm

    def get_queryset(self, request):
        qs = super(SolutionAdmin, self).get_queryset(request)
        qs = qs.solution_with_count_tags_links_opinions_comments_quality_scopes()
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
    get_count_tags.short_description = _('Count tags')
    get_count_tags.admin_order_field = 'count_tags'

    def colored_quality(self, obj):
        details = obj.get_detail_about_quality()
        color = details.color
        return format_html('<span style="color: {1};">{0}</span>', obj.quality, color)
    colored_quality.short_description = _('Quality')
    colored_quality.admin_order_field = 'scope'
