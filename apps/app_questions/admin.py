
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db import models

from apps.app_generic_models.admin import OpinionGenericInline, CommentGenericInline, LikeGenericInline

from .forms import QuestionForm
from .models import Answer


class AnswerInline(admin.StackedInline):
    '''
    Stacked Inline View for Answer
    '''

    model = Answer
    extra = 0
    fk_name = 'question'
    fields = ['author', 'is_accepted', 'text_answer']


class QuestionAdmin(admin.ModelAdmin):
    '''
    Admin View for Question
    '''

    list_display = (
        'title',
        'author',
        'status',
        'get_count_answers',
        'has_accepted_answer',
        'get_scope2',
        # 'get_scope',
        'get_count_opinions',
        'get_count_tags',
        'is_dublicated',
        'is_new',
        'last_activity',
        'date_modified',
        'date_added')
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        'status',
        'date_modified',
        'date_added',
        'is_dublicated',
    )
    inlines = [
        OpinionGenericInline,
        AnswerInline,
    ]
    fieldsets = [
        (_('Question'), {
            'fields': ['title', 'author', 'status', 'text_question', 'is_dublicated', 'tags'],
        }),
    ]
    filter_horizontal = ['tags']
    form = QuestionForm
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_answers=models.Count('answers', distinct=True),
            count_tags=models.Count('tags', distinct=True),
            count_opinions=models.Count('opinions', distinct=True),
            # scope=models.Sum(
            #     models.Case(
            #         models.When(opinions__is_useful=True, then=1),
            #         models.When(opinions__is_useful=False, then=-1),
            #         output_field=models.IntegerField()
            #     ), distinct=True
            # ),
        )
        (setattr(i, 'scope', i.get_scope()) for i in qs)
        return qs

    def get_count_answers(self, obj):
        return obj.count_answers
    get_count_answers.admin_order_field = 'count_answers'
    get_count_answers.short_description = _('Count answers')

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_scope2(self, obj):
        return obj.scope
    get_scope2.admin_order_field = 'scope'
    get_scope2.short_description = _('Scope')


class AnswerAdmin(admin.ModelAdmin):
    '''
        Admin View for Answer
    '''

    list_display = (
        'question',
        'author',
        'is_accepted',
        # 'get_count_comments',
        # 'get_count_likes',
        'get_scope',
        'myscope',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('question', admin.RelatedOnlyFieldListFilter),
        'is_accepted',
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    inlines = [
        LikeGenericInline,
        CommentGenericInline,
    ]
    fields = ['question', 'author', 'text_answer', 'is_accepted']

    def get_queryset(self, request):
        qs = super(AnswerAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_likes=models.Count('likes', distinct=True),
            count_comments=models.Count('comments', distinct=True),
            scope=models.Sum(
                models.Case(
                    models.When(likes__liked_it=True, then=1),
                    models.When(likes__liked_it=False, then=-1),
                    output_field=models.IntegerField()
                ),
            ),
        )
        return qs

    def get_count_likes(self, obj):
        return obj.count_likes
    get_count_likes.admin_order_field = 'count_likes'
    get_count_likes.short_description = _('Count likes')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def myscope(self, obj):
        return obj.scope
