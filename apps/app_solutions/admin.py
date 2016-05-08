
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Count

from apps.app_generic_models.admin import OpinionGenericInline, CommentGenericInline

from .forms import SolutionForm
from .models import Solution


class SolutionInline(admin.StackedInline):
    '''
    Tabular Inline View for Solution
    '''

    # inline Opinions
    model = Solution
    extra = 1
    fk_name = 'category'
    fieldsets = [
        [None, {
            'fields': ['title', 'body', 'tags', 'useful_links']
        }]
    ]
    filter_vertical = ['useful_links']
    filter_horizontal = ['tags']


class SolutionCategoryAdmin(admin.ModelAdmin):
    """
    Admin View for SolutionCategory
    """

    list_display = ('name', 'lexer', 'get_count_solutions', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('lexer', admin.AllValuesFieldListFilter),
        'date_modified',
        'date_added',
    )
    # list_editable = ['lexer']
    date_hierarchy = 'date_added'
    search_fields = ('name',)
    inlines = [
        SolutionInline,
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
        'get_count_useful_links',
        # 'get_count_good_opinions',
        # 'get_count_bad_opinions',
        # 'get_count_favorites',
        'get_count_opinions',
        'get_count_comments',
        'get_count_tags',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        'date_modified',
        'date_added',
        ('category', admin.RelatedFieldListFilter),
    )
    search_fields = ('title',)
    date_hierarchy = 'date_added'
    inlines = [
        OpinionGenericInline,
        CommentGenericInline,
    ]
    fields = ['title', 'category', 'body', 'useful_links', 'tags']
    filter_horizontal = ['tags']
    filter_vertical = ['useful_links']
    form = SolutionForm

    def get_queryset(self, request):
        qs = super(SolutionAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_useful_links=Count('useful_links', distinct=True),
            count_opinions=Count('opinions', distinct=True),
            count_comments=Count('comments', distinct=True),
            count_tags=Count('tags', distinct=True),
        )
        return qs

    def get_count_useful_links(self, obj):
        return obj.count_useful_links
    get_count_useful_links.short_description = _('Count links')
    get_count_useful_links.admin_order_field = 'count_useful_links'

    # def get_count_good_opinions(self, obj):
    #     return UserComment_Generic.objects.filter() obj.opinions.through.objects.filter(solution=obj, is_useful=True).count()
    # get_count_good_opinions.short_description = _('Count good opinions')

    # def get_count_bad_opinions(self, obj):
    #     return obj.opinions.through.objects.filter(solution=obj, is_useful=False).count()
    # get_count_bad_opinions.short_description = _('Count bad opinions')

    # def get_count_favorites(self, obj):
    #     return obj.opinions.through.objects.filter(solution=obj, is_favorite=obj.opinions.through.CHOICES_FAVORITE.yes).count()
    # get_count_favorites.short_description = _('Count favorites')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.short_description = _('Total count opinions')
    get_count_opinions.admin_order_field = 'count_opinions'

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.short_description = _('Count comments')
    get_count_comments.admin_order_field = 'count_comments'

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')
