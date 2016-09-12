
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db import models

# from apps.generic_models.admin import OpinionGenericInline, CommentGenericInline

from .forms import QuestionForm
from .models import Answer


class AnswerInline(admin.StackedInline):
    '''
    Stacked Inline View for Answer
    '''

    model = Answer
    extra = 0
    fk_name = 'question'
    fields = ['user', 'is_accepted', 'text_answer']


class QuestionAdmin(admin.ModelAdmin):
    '''
    Admin View for Question
    '''

    list_display = (
        'title',
        'user',
        'status',
        'get_count_answers',
        'has_accepted_answer',
        'get_rating',
        'get_count_opinions',
        'get_count_tags',
        'get_count_flavours',
        'is_new',
        'get_latest_activity',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'status',
        'date_modified',
        'date_added',
    )
    inlines = [
        # OpinionGenericInline,
        AnswerInline,
    ]
    fieldsets = [
        (_('Question'), {
            'fields': ['title', 'user', 'status', 'text_question', 'tags'],
        }),
    ]
    filter_horizontal = ['tags']
    form = QuestionForm
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        qs = qs.queryset_with_all_additional_fields()
        return qs


class AnswerAdmin(admin.ModelAdmin):
    '''
        Admin View for Answer
    '''

    list_display = (
        'question',
        'user',
        'is_accepted',
        # 'get_count_comments',
        # 'get_count_likes',
        'get_rating',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('question', admin.RelatedOnlyFieldListFilter),
        'is_accepted',
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    inlines = [
        # CommentGenericInline,
    ]
    fields = ['question', 'user', 'text_answer', 'is_accepted']

    def get_queryset(self, request):
        qs = super(AnswerAdmin, self).get_queryset(request)
        qs = qs.queryset_with_all_additional_fields()
        return qs

    def get_count_likes(self, obj):
        return obj.count_likes
    get_count_likes.admin_order_field = 'count_likes'
    get_count_likes.short_description = _('Count likes')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')
