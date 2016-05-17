
from django.db import models
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
        'get_scope2',
        'get_good_opinions',
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
            count_tags=models.Count('tags', distinct=True),
            count_comments=models.Count('comments', distinct=True),
            count_opinions=models.Count('opinions', distinct=True),
            scope=models.Count('opinions', distinct=True),
            count_good_opinions=models.Count(
                models.Case(
                    models.When(opinions__is_useful=True, then=True),
                    ouput_field=models.BooleanField(),
                ),
                distinct=True,
            ),
        )
        (setattr(i, 'scope', 111111) for i in qs)
        for i in qs:
            i.scope = 11111111111111111
        # import ipdb; ipdb.set_trace()
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

    def get_good_opinions(self, obj):
        return obj.count_good_opinions
    get_good_opinions.admin_order_field = 'count_good_opinions'
    get_good_opinions.short_description = _('Count good opinions')

    def get_scope2(self, obj):
        return obj.scope
    get_scope2.admin_order_field = 'scope'
    get_scope2.short_description = _('Scope2')
