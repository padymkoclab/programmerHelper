
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from mylabour.listfilters import IsNewSimpleListFilter

from .models import Suit, TestQuestion, Variant, Passage
from .formsets import VariantInlineFormSet
from .forms import SuitAdminModelForm, TestQuestionAdminInlineModelForm, TestQuestionAdminModelForm, VariantAdminModelForm


class TestQuestionInline(admin.StackedInline):
    """
    Stacked Inline View for TestQuestion
    """

    form = TestQuestionAdminInlineModelForm
    model = TestQuestion
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
    min_num = TestQuestion.MIN_COUNT_VARIANTS_FOR_FULL_QUESTION
    max_num = TestQuestion.MAX_COUNT_VARIANTS_FOR_FULL_QUESTION
    extra = 0
    fk_name = 'question'
    can_delete = True
    formset = VariantInlineFormSet


class PassageInline(admin.TabularInline):
    """
    Stacked Inline View for TestQuestion
    """

    model = Suit.passages.through
    extra = 0
    can_delete = False
    fields = ['user', 'status', 'mark', 'date_passage']
    readonly_fields = ['user', 'status', 'mark', 'date_passage']
    classes = ['collapse']


class SuitAdmin(admin.ModelAdmin):
    """
    Admin View for Suit
    """

    form = SuitAdminModelForm
    search_fields = ('name', )
    list_display = (
        'truncated_name',
        'colored_status',
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
    fieldsets = [
        [
            Suit._meta.verbose_name, {
                'fields': ['name', 'slug', 'status', 'image', 'duration', 'complexity', 'description'],
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(SuitAdmin, self).get_queryset(request)
        qs = qs
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [TestQuestionInline]

            if obj.questions.exists():
                inlines += [PassageInline]

            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def truncated_name(self, obj):
        return truncatechars(obj.name, 50)
    truncated_name.short_description = Suit._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'

    def colored_status(self, obj):
        if obj.status == Suit.COMPLETED:
            color = 'rgb(0, 255, 0)'
        elif obj.status == Suit.UNCOMPLETED:
            color = 'rgb(255, 0, 0)'
        return format_html('<span style="color: {}">{}</span>', color, obj.status)
    colored_status.short_description = Suit._meta.get_field('status').verbose_name
    colored_status.admin_order_field = 'status'


class TestQuestionAdmin(admin.ModelAdmin):
    """
    Admin View for TestQuestion
    """

    form = TestQuestionAdminModelForm
    search_fields = ('title',)
    list_display = ('truncated_text_question', 'truncated_suit', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('suit', admin.RelatedOnlyFieldListFilter),
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    fieldsets = [
        [
            TestQuestion._meta.verbose_name, {
                'fields': ['title', 'slug', 'suit', 'text_question'],
            }
        ]
    ]
    prepopulated_fields = {'slug': ('title', )}

    def get_queryset(self, request):
        qs = super(TestQuestionAdmin, self).get_queryset(request)
        qs = qs
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [VariantInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def truncated_suit(self, obj):
        return truncatechars(obj.suit, 50)
    truncated_suit.short_description = TestQuestion._meta.get_field('suit').verbose_name
    truncated_suit.admin_order_field = 'suit'

    def truncated_text_question(self, obj):
        return truncatechars(obj.text_question, 50)
    truncated_text_question.short_description = TestQuestion._meta.get_field('text_question').verbose_name
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

    list_display = ['truncated_suit', 'user', 'colored_status', 'mark', 'date_passage']
    date_hierarchy = 'date_passage'
    list_filter = [
        ('suit', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'status',
        'date_passage',
    ]
    fieldsets = [
        [
            Passage._meta.verbose_name, {
                'fields': ['suit', 'user', 'status', 'mark'],
            }
        ]
    ]
    readonly_fields = ['suit', 'user', 'status', 'mark']

    def truncated_suit(self, obj):
        return truncatechars(obj.suit, 60)
    truncated_suit.short_description = Passage._meta.get_field('suit').verbose_name
    truncated_suit.admin_order_field = 'suit'

    def colored_status(self, obj):
        if obj.status == Passage.PASSED:
            color = 'rgb(0, 255, 0)'
        elif obj.status == Passage.ATTEMPT:
            color = 'rgb(255, 0, 0)'
        return format_html('<span style="color: {}">{}</span>', color, obj.status)
    colored_status.short_description = Passage._meta.get_field('status').verbose_name
    colored_status.admin_order_field = 'status'
