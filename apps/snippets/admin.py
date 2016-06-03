
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.comments.admin import CommentInline
from apps.opinions.admin import OpinionInline
from apps.favours.admin import FavourInline

from .models import Snippet
from .forms import SnippetForm


class SnippetAdmin(admin.ModelAdmin):
    '''
    Admin View for Snippet
    '''

    form = SnippetForm
    list_display = (
        'title',
        'account',
        'lexer',
        # 'views',
        'get_scope',
        'get_count_comments',
        'get_count_tags',
        'get_count_good_opinions',
        'get_count_bad_opinions',
        'get_count_opinions',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        'lexer',
        'date_modified',
        'date_added',
    )
    inlines = [
        OpinionInline,
        FavourInline,
        CommentInline,
    ]
    search_fields = ('title',)
    filter_horizontal = ['tags']
    date_hierarchy = 'date_modified'
    fieldsets = [
        [
            Snippet._meta.verbose_name, {
                'fields': ['title', 'account', 'lexer', 'description', 'code', 'tags']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(SnippetAdmin, self).get_queryset(request)
        qs = qs.snippets_with_total_counters_on_related_fields()
        return qs

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_good_opinions(self, obj):
        return obj.count_good_opinions
    get_count_good_opinions.admin_order_field = 'count_good_opinions'
    get_count_good_opinions.short_description = _('Count good opinions')

    def get_count_bad_opinions(self, obj):
        return obj.count_bad_opinions
    get_count_bad_opinions.admin_order_field = 'count_bad_opinions'
    get_count_bad_opinions.short_description = _('Count bad opinions')
