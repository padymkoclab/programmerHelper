
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.datetime_utils import convert_date_to_django_date_format
from utils.django.listfilters import IsNewSimpleListFilter

from apps.core.admin import AppAdmin
from apps.comments.admin import CommentGenericInline
from apps.opinions.admin import OpinionGenericInline
from apps.flavours.admin import FlavourGenericInline

from .forms import QuestionAdminModelForm, AnswerAdminModelForm, AnswerInlineAdminModelForm
from .models import Question, Answer
from .listfilters import HasAcceptedAnswerSimpleListFilter, LatestActivitySimpleListFilter
from .apps import QuestionsConfig


class QuestionsAppAdmin(AppAdmin):

    label = QuestionsConfig.label

    def get_context_for_tables_of_statistics(self):

        return (
            (
                _('Questions'), (
                    (_('Count questions'), Question.objects.count()),
                    (_('Average count answers'), Question.objects.get_avg_count_answers()),
                ),
            ),
            (
                _('Answers'), (
                    (_('Count answers'), Answer.objects.count()),
                ),
            ),
            (
                _('Opinions to questions'), (
                    (_('Count opinions'), Question.opinions_manager.get_count_opinions()),
                    (_('Average count opinions'), Question.opinions_manager.get_avg_count_opinions()),
                    (_('Count critics'), Question.opinions_manager.get_count_critics()),
                    (_('Count supporters'), Question.opinions_manager.get_count_supporters()),
                ),
            ),
            (
                _('Opinions to answers'), (
                    (_('Count opinions'), Answer.opinions_manager.get_count_opinions()),
                    (_('Average count opinions'), Answer.opinions_manager.get_avg_count_opinions()),
                    (_('Count critics'), Answer.opinions_manager.get_count_critics()),
                    (_('Count supporters'), Answer.opinions_manager.get_count_supporters()),
                ),
            ),
            (
                _('Flavours to questions'), (
                    (_('Count flavours'), Question.flavours_manager.get_count_flavours()),
                ),
            ),
            (
                _('Comments to answers'), (
                    (_('Count comments'), Answer.comments_manager.get_count_comments()),
                    (_('Average count comments'), Answer.comments_manager.get_avg_count_comments()),
                    (_('Count distinct users posted comments'),
                        Answer.comments_manager.get_count_distinct_users_posted_comments()),
                ),
            ),
            (
                _('Tags to questions'), (
                    (_('Count usaged tags'), Question.tags_manager.get_count_usaged_tags()),
                    (_('Average count tags'), Question.tags_manager.get_avg_count_tags()),
                    (_('Count unique usaged tags'), Question.tags_manager.get_count_unique_usaged_tags()),
                )
            ),
        )

    def get_context_for_charts_of_statistics(self):

        return (
            {
                'title': _('Chart count questions for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count questions')),
                    'data': Question.objects.get_statistics_count_questions_for_the_past_year(),
                },
                'chart': Question.objects.get_chart_count_questions_for_the_past_year(),
            },
            {
                'title': _('Chart count answers for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count answers')),
                    'data': Answer.objects.get_statistics_count_answers_for_the_past_year(),
                },
                'chart': Answer.objects.get_chart_count_answers_for_the_past_year(),
            },
            {
                'title': _('Chart count comments to answers for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count comments')),
                    'data': Answer.comments_manager.get_statistics_count_comments_for_the_past_year(),
                },
                'chart': Answer.comments_manager.get_chart_count_comments_for_the_past_year(),
            },
            {
                'title': _('Chart count opinions to questions for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count opinions')),
                    'data': Question.opinions_manager.get_statistics_count_opinions_for_the_past_year(),
                },
                'chart': Question.opinions_manager.get_chart_count_opinions_for_the_past_year(),
            },
            {
                'title': _('Chart count opinions to answers for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count opinions')),
                    'data': Answer.opinions_manager.get_statistics_count_opinions_for_the_past_year(),
                },
                'chart': Answer.opinions_manager.get_chart_count_opinions_for_the_past_year(),
            },
            {
                'title': _('Chart count flavours to questions for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count flavours')),
                    'data': Question.flavours_manager.get_statistics_count_flavours_for_the_past_year(),
                },
                'chart': Question.flavours_manager.get_chart_count_flavours_for_the_past_year(),
            },
        )


class AnswerInline(admin.StackedInline):
    '''
    Stacked Inline View for Answer
    '''

    form = AnswerInlineAdminModelForm
    model = Answer
    extra = 0
    fk_name = 'question'
    fieldsets = (
        (
            None, {
                'fields': (
                    'user',
                    'is_accepted',
                )
            }
        ),
        (
            None, {
                'classes': ('full-width', ),
                'fields': ('text_answer', )
            }
        ),
    )
    readonly_fields = (
        'get_rating',
        'get_count_opinions',
        'get_count_comments',
        'date_modified',
        'date_added',
    )


class QuestionAdmin(admin.ModelAdmin):
    '''
    Admin View for Question
    '''

    list_display = (
        'truncated_title',
        'user',
        'status',
        'get_count_answers',
        'has_accepted_answer',
        'get_rating',
        'get_count_opinions',
        'get_count_tags',
        'get_count_flavours',
        'is_new',
        'get_date_latest_activity',
        'date_added',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'status',
        HasAcceptedAnswerSimpleListFilter,
        IsNewSimpleListFilter,
        LatestActivitySimpleListFilter,
        'date_added',
    )
    filter_horizontal = ('tags', )
    form = QuestionAdminModelForm
    search_fields = ('title', )
    readonly_fields = (
        'get_count_answers',
        'has_accepted_answer',
        'get_rating',
        'get_count_opinions',
        'get_count_tags',
        'get_count_flavours',
        'get_count_like_flavours',
        'get_count_dislike_flavours',
        'get_date_latest_activity_for_admin_readonly',
        'date_added',
        'date_modified',
    )

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        qs = qs.queryset_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                Question._meta.verbose_name, {
                    'fields': [
                        'title',
                        'slug',
                        'user',
                        'status',
                        'tags',
                    ],
                }
            ),
            (
                Question._meta.get_field('text_question').verbose_name, {
                    'classes': ('full-width', ),
                    'fields': ('text_question', ),
                }
            ),
        ]

        if obj is not None:

            fieldsets.append(
                (
                    _('Additional information'), {
                        'classes': ('collapse', ),
                        'fields': (
                            'get_count_answers',
                            'has_accepted_answer',
                            'get_rating',
                            'get_count_opinions',
                            'get_count_tags',
                            'get_count_flavours',
                            'get_count_like_flavours',
                            'get_count_dislike_flavours',
                            'get_date_latest_activity_for_admin_readonly',
                            'date_added',
                            'date_modified',
                        )
                    }
                )
            )

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            inlines = [OpinionGenericInline, FlavourGenericInline, AnswerInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def suit_cell_attributes(self, obj, column):

        if column in ['truncated_title']:
            return {'class': 'text-left'}
        elif column in ['date_added', 'date_modified']:
            return {'class': 'text-right'}
        return {'class': 'text-center'}

    def suit_row_attributes(self, obj, request):

        rating = obj.get_rating()

        if rating is not None:
            if rating > 0:
                return {'class': 'success'}
            elif rating < 0:
                return {'class': 'error'}

    def truncated_title(self, obj):
        """ """

        return truncatechars(obj.title, 70)
    truncated_title.short_description = Question._meta.get_field('title').verbose_name
    truncated_title.admin_order_field = 'title'

    def get_date_latest_activity_for_admin_readonly(self, obj):
        """ """

        return convert_date_to_django_date_format(obj.get_date_latest_activity())
    get_date_latest_activity_for_admin_readonly.short_description = _('Date latest activity')


class AnswerAdmin(admin.ModelAdmin):
    '''
    Admin View for Answer
    '''

    list_display = (
        'truncated_question',
        'user',
        'is_accepted',
        'get_rating',
        'get_count_opinions',
        'get_count_comments',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('question', admin.RelatedOnlyFieldListFilter),
        'is_accepted',
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    form = AnswerAdminModelForm
    date_hierarchy = 'date_added'
    readonly_fields = (
        'get_rating',
        'get_count_opinions',
        'get_count_comments',
        'date_modified',
        'date_added',
    )

    def get_queryset(self, request):
        qs = super(AnswerAdmin, self).get_queryset(request)
        qs = qs.queryset_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                Answer._meta.verbose_name, {
                    'fields': [
                        'question',
                        'user',
                        'is_accepted',
                    ]
                }
            ),
            (
                Answer._meta.get_field('text_answer').verbose_name, {
                    'classes': ('full-width', ),
                    'fields': ('text_answer', ),
                }
            ),
        ]

        if obj is not None:

            fieldsets.append(
                (
                    _('Additional information'), {
                        'classes': ('collapse', ),
                        'fields': (
                            'get_rating',
                            'get_count_opinions',
                            'get_count_comments',
                            'date_modified',
                            'date_added',
                        )
                    }
                )
            )

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            inlines = [CommentGenericInline, OpinionGenericInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def suit_cell_attributes(self, obj, column):

        if column in ['truncated_question']:
            return {'class': 'text-left'}
        elif column in ['date_added', 'date_modified']:
            return {'class': 'text-right'}
        return {'class': 'text-center'}

    def suit_row_attributes(self, obj, request):

        rating = obj.get_rating()

        if rating is not None:
            if rating > 0:
                return {'class': 'success'}
            elif rating < 0:
                return {'class': 'error'}

    def truncated_question(self, obj):
        """ """

        return truncatechars(obj.question, 70)
    truncated_question.short_description = Answer._meta.get_field('question').verbose_name
    truncated_question.admin_order_field = 'question'
