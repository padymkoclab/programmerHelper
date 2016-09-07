
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.html import format_html

from utils.django.listfilters import LatestActivityListFilter
from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from .listfilters import QualityListFilter
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
    prepopulated_fields = {'slug': ['name']}
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
        'problem',
        'category',
        'user',
        'get_scope',
        'colored_quality',
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
        ('user', admin.RelatedOnlyFieldListFilter),
        QualityListFilter,
        'date_modified',
        'date_added',
    )
    search_fields = ('problem',)
    date_hierarchy = 'date_added'
    inlines = [
        OpinionGenericInline,
        CommentGenericInline,
    ]
    fieldsets = [
        [
            Solution._meta.verbose_name, {
                'fields': ['problem', 'slug', 'category', 'user', 'body', 'tags', 'links'],
            }
        ],
    ]
    filter_horizontal = ['tags']
    # filter_vertical = ['links']
    prepopulated_fields = {'slug': ['problem']}
    form = SolutionForm

    def get_queryset(self, request):
        qs = super(SolutionAdmin, self).get_queryset(request)
        qs = qs.solutions_with_count_tags_links_opinions_comments_and_quality_scopes()
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
        quality = obj.get_quality()
        if quality == 'Approved':
            color = 'darkgreen'
        elif quality == 'Good':
            color = 'lightgreen'
        elif quality == 'Vague':
            color = 'black'
        elif quality == 'Bad':
            color = 'red'
        elif quality == 'Heinously':
            color = 'darkred'
        return format_html('<span style="color: {1};">{0}</span>', obj.quality, color)
    colored_quality.short_description = _('Quality')
    colored_quality.admin_order_field = 'scope'
