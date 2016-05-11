
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.app_generic_models.admin import OpinionGenericInline, CommentGenericInline

from .models import Snippet
from .forms import SnippetForm


class SnippetAdmin(admin.ModelAdmin):
    '''
    Admin View for Snippet
    '''

    form = SnippetForm
    list_display = (
        'title',
        'author',
        'lexer',
        'views',
        'get_scope',
        'get_count_comments',
        'get_count_opinions',
        'get_count_tags',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        'lexer',
        'date_modified',
        'date_added',
    )
    inlines = [
        OpinionGenericInline,
        CommentGenericInline,
    ]
    search_fields = ('title',)
    filter_horizontal = ['tags']
    date_hierarchy = 'date_modified'
    fieldsets = [
        [
            Snippet._meta.verbose_name, {
                'fields': ['title', 'author', 'lexer', 'description', 'code', 'tags']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(SnippetAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_tags=Count('tags', distinct=True),
            count_comments=Count('comments', distinct=True),
            count_opinions=Count('opinions', distinct=True),
            # count_good_opinions=Count(
            #     Case(
            #         When(opinionaboutsnippet__is_useful=True, then=True),
            #         default=None,
            #         ouput_field=BooleanField(),
            #     ),
            # distinct=True
            # )
        )
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
