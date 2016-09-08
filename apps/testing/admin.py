
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.admin_utils import remove_url_from_admin_urls
from utils.django.listfilters import IsNewSimpleListFilter

from .models import Suit, Question, Variant, Passage
from .formsets import QuestionInlineFormSet, VariantInlineFormSet
from .forms import (
    SuitAdminModelForm,
    QuestionAdminInlineModelForm,
    QuestionAdminModelForm,
    VariantAdminModelForm,
)
from .listfilters import IsCompletedSimpleListFilter


class TestingAppAdmin:

    def add_statistics_data_to_context(self, context):
        """Add statictis data to a context."""

        context['statistics_data'] = {
            'count_suits': Suit.objects.count(),
            'count_passages': Passage.objects.count(),
            'count_questions': Question.objects.count(),
            'count_variants': Variant.objects.count(),
            'avg_count_questions_for_suits': Suit.objects.get_avg_count_questions(),
            'avg_count_passages_for_suits': Suit.objects.get_avg_count_passages(),
            'avg_count_variants_in_questions': Question.objects.get_avg_count_variants_in_questions(),
            'count_attempt_passages': Passage.objects.get_count_attempt_passages(),
            'count_passed_passages': Passage.objects.get_count_passed_passages(),
            'count_distinct_testers': Passage.objects.get_count_distinct_testers(),
            'avg_mark_for_passages': Passage.objects.get_avg_mark_passages(),
            'chart_count_passages_for_the_past_year': Passage.objects.get_chart_count_passages_for_the_past_year(),
            'statistics_count_passages_by_the_past_year': Passage.objects.get_statistics_count_passages_by_the_past_year(),
        }

    def add_context_to_report_page(self, context):

        # context with statictis data
        context['themes_for_reports'] = {
            Question._meta.verbose_name_plural: 'questions',
            Passage._meta.verbose_name_plural: 'passages',
            Variant._meta.verbose_name_plural: 'variants',
            Suit._meta.verbose_name_plural: 'suits',
        }

    def get_report(self, output_report, themes):

        msg = 'Report must generated in {0} on themes: {1}'.format(output_report.upper(), themes)
        return msg


class QuestionInline(admin.StackedInline):
    """
    Stacked Inline View for Question
    """

    formset = QuestionInlineFormSet
    form = QuestionAdminInlineModelForm
    model = Question
    min_num = Suit.MIN_COUNT_QUESTIONS_FOR_COMPLETED_SUIT
    max_num = Suit.MAX_COUNT_QUESTIONS_FOR_COMPLETED_SUIT
    extra = 0
    can_delete = True
    fk_name = 'suit'
    fields = ['title', 'slug', 'text_question']
    classes = ['collapse']


class VariantInline(admin.TabularInline):
    """
    Tabular Inline View for Variant
    """

    classes = ['collapse']
    form = VariantAdminModelForm
    model = Variant
    min_num = Question.MIN_COUNT_VARIANTS_FOR_FULL_QUESTION
    max_num = Question.MAX_COUNT_VARIANTS_FOR_FULL_QUESTION
    extra = 0
    fk_name = 'question'
    can_delete = True
    formset = VariantInlineFormSet


class PassageInline(admin.TabularInline):
    """
    Stacked Inline View for Question
    """

    model = Suit.testers.through
    extra = 0
    can_delete = False
    fields = ['user', 'status', 'mark', 'date']
    readonly_fields = ['user', 'status', 'mark', 'date']
    classes = ['collapse']


class SuitAdmin(admin.ModelAdmin):
    """
    Admin View for Suit
    """

    form = SuitAdminModelForm
    search_fields = ('name', )
    list_display = (
        'truncated_name',
        'status',
        'get_count_questions',
        'get_count_passages',
        'duration',
        'complexity',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        'status',
        'complexity',
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )

    date_hierarchy = 'date_added'
    readonly_fields = [
        'get_count_questions',
        'get_count_passages',
        'get_count_attempt_passages',
        'get_count_passed_passages',
        'get_count_distinct_testers',
        'get_avg_mark',
        'date_modified',
        'date_added'
    ]
    prepopulated_fields = {'slug': ('name', )}

    def get_queryset(self, request):
        qs = super(SuitAdmin, self).get_queryset(request)
        qs = qs.suits_with_all_additional_fields()
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [QuestionInline]

            if obj.questions.exists():
                inlines += [PassageInline]

            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Suit._meta.verbose_name, {
                    'fields': [
                        'name',
                        'slug',
                        'status',
                        'image',
                        'duration',
                        'complexity',
                        'description',
                    ],
                }
            ]
        ]

        if obj is not None:

            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_count_questions',
                        'get_count_passages',
                        'get_count_attempt_passages',
                        'get_count_passed_passages',
                        'get_count_distinct_testers',
                        'get_avg_mark',
                        'date_modified',
                        'date_added',
                    ]
                }
            ])

        return fieldsets

    def truncated_name(self, obj):
        return truncatechars(obj.name, 50)
    truncated_name.short_description = Suit._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'


class QuestionAdmin(admin.ModelAdmin):
    """
    Admin View for Question
    """

    form = QuestionAdminModelForm
    search_fields = ('title',)
    list_display = (
        'truncated_text_question',
        'truncated_suit',
        'get_count_variants',
        'is_completed',
        'is_new',
        'date_modified',
        'date_added'
    )
    list_filter = (
        ('suit', admin.RelatedOnlyFieldListFilter),
        IsCompletedSimpleListFilter,
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ('title', )}
    readonly_fields = ['get_count_variants', 'is_completed', 'date_modified', 'date_added']

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        qs = qs.questions_with_all_additional_fields()
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [VariantInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Question._meta.verbose_name, {
                    'fields': ['title', 'slug', 'suit', 'text_question'],
                }
            ]
        ]

        if obj is not None:
            fieldsets.append([
                _("Additional information"), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_count_variants',
                        'is_completed',
                        'date_modified',
                        'date_added'
                    ]
                }
            ])

        return fieldsets

    def truncated_suit(self, obj):
        return truncatechars(obj.suit, 50)
    truncated_suit.short_description = Question._meta.get_field('suit').verbose_name
    truncated_suit.admin_order_field = 'suit'

    def truncated_text_question(self, obj):
        return truncatechars(obj.text_question, 50)
    truncated_text_question.short_description = Question._meta.get_field('text_question').verbose_name
    truncated_text_question.admin_order_field = 'text_question'


class VariantAdmin(admin.ModelAdmin):
    '''
        Admin View for Variant
    '''

    # form = VariantAdminModelForm
    list_display = ('truncated_text_variant', 'truncated_question', 'is_right_variant')
    list_filter = (
        ('question', admin.RelatedOnlyFieldListFilter),
        ('is_right_variant', admin.BooleanFieldListFilter),
    )
    search_fields = ('question__title',)
    fieldsets = [
        [
            Variant._meta.verbose_name, {
                'fields': ['question', 'text_variant', 'is_right_variant'],
            }
        ]
    ]

    def get_urls(self):

        urls = super().get_urls()

        urls += [
        ]

        remove_url_from_admin_urls(urls, 'add'),
        remove_url_from_admin_urls(urls, 'change'),
        remove_url_from_admin_urls(urls, 'history'),
        remove_url_from_admin_urls(urls, 'delete'),

        return urls

    def truncated_text_variant(self, obj):
        return truncatechars(obj, 70)
    truncated_text_variant.short_description = Variant._meta.get_field('text_variant').verbose_name
    truncated_text_variant.admin_order_field = 'text_variant'

    def truncated_question(self, obj):
        return truncatechars(obj.question, 70)
    truncated_question.short_description = Variant._meta.get_field('question').verbose_name
    truncated_question.admin_order_field = 'question'


class PassageAdmin(admin.ModelAdmin):
    """

    """

    list_display = ['truncated_suit', 'user', 'colored_status', 'mark', 'date']
    date_hierarchy = 'date'
    list_filter = [
        ('suit', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'status',
        'date',
    ]
    fieldsets = [
        [
            Passage._meta.verbose_name, {
                'fields': ['suit', 'user', 'status', 'mark'],
            }
        ]
    ]
    readonly_fields = ['suit', 'user', 'status', 'mark']

    def get_urls(self):

        urls = super().get_urls()

        urls += [
        ]

        remove_url_from_admin_urls(urls, 'add'),
        remove_url_from_admin_urls(urls, 'change'),
        remove_url_from_admin_urls(urls, 'history'),
        remove_url_from_admin_urls(urls, 'delete'),

        return urls

    def truncated_suit(self, obj):
        return truncatechars(obj.suit, 60)
    truncated_suit.short_description = Passage._meta.get_field('suit').verbose_name
    truncated_suit.admin_order_field = 'suit'

    def colored_status(self, obj):
        if obj.status == Passage.PASSED:
            color = 'rgb(0, 255, 0)'
        elif obj.status == Passage.ATTEMPT:
            color = 'rgb(255, 0, 0)'
        return format_html('<span style="color: {}">{}</span>', color, obj.get_status_display())
    colored_status.short_description = Passage._meta.get_field('status').verbose_name
    colored_status.admin_order_field = 'status'
