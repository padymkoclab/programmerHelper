
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from .models import TestQuestion, Variant
from .forms import VariantInlineFormSet


class QuestionInline(admin.StackedInline):
    """
    Stacked Inline View for Question
    """

    model = TestQuestion
    max_num = 20
    extra = 3
    fk_name = 'test_suit'


class TestSuitAdmin(admin.ModelAdmin):
    """
    Admin View for TestSuit
    """

    search_fields = ('name',)
    list_display = (
        'name',
        'author',
        'duration',
        'complexity',
        'count_attempts_passing',
        'count_completed_passing',
        'get_count_questions',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        'complexity',
        'date_modified',
        'date_added',
        ('author', admin.RelatedOnlyFieldListFilter),
    )
    inlines = [
        QuestionInline,
    ]

    def get_queryset(self, request):
        qs = super(TestSuitAdmin, self).get_queryset(request)
        qs = qs.annotate(count_questions=Count('questions', distinct=True))
        return qs

    def get_count_questions(self, obj):
        return obj.count_questions
    get_count_questions.admin_order_field = 'count_questions'
    get_count_questions.short_description = _('Count questions')


class VariantInline(admin.TabularInline):
    """
    Tabular Inline View for Variant
    """

    model = Variant
    min_num = 3
    max_num = 6
    extra = 1
    fk_name = 'question'
    formset = VariantInlineFormSet


class TestQuestionAdmin(admin.ModelAdmin):
    """
    Admin View for TestQuestion
    """

    search_fields = ('name',)
    list_display = ('name', 'test_suit', 'is_new', 'get_count_variants', 'date_modified', 'date_added')
    list_filter = (
        'date_modified',
        'date_added',
        ('test_suit', admin.RelatedOnlyFieldListFilter),
    )
    inlines = [
        VariantInline,
    ]

    def get_queryset(self, request):
        qs = super(TestQuestionAdmin, self).get_queryset(request)
        qs = qs.annotate(count_variants=Count('variants', distinct=True))
        return qs

    def get_count_variants(self, obj):
        return obj.count_variants
    get_count_variants.admin_order_field = 'count_variants'
    get_count_variants.short_description = _('Count variants')


class VariantAdmin(admin.ModelAdmin):
    '''
        Admin View for Variant
    '''
    list_display = ('question', 'is_right_variant')
    list_filter = (
        ('question', admin.RelatedOnlyFieldListFilter),
        ('is_right_variant', admin.BooleanFieldListFilter),
    )
    search_fields = ('question__title',)
