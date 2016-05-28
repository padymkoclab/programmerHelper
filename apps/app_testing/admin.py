
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from .models import TestingSuit, TestingQuestion, TestingVariant, TestingPassage
from .forms import TestingVariantInlineFormSet


class TestingQuestionInline(admin.StackedInline):
    """
    Stacked Inline View for Question
    """

    model = TestingQuestion
    max_num = 20
    min_num = 3
    extra = 0
    fk_name = 'testing_suit'
    fields = ['title', 'text_question']


class TestingPassageInline(admin.TabularInline):
    """
    Stacked Inline View for Question
    """

    model = TestingSuit.passages.through
    extra = 0
    fields = ['account', 'status', 'scope']


class TestingSuitAdmin(admin.ModelAdmin):
    """
    Admin View for TestingSuit
    """

    search_fields = ('name',)
    list_display = (
        'name',
        'account',
        'duration',
        'complexity',
        'count_attempts_passing',
        'count_completed_passing',
        'get_avg_scope_by_completed_passing',
        'get_count_questions',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        'complexity',
        'date_modified',
        'date_added',
        ('account', admin.RelatedOnlyFieldListFilter),
    )
    inlines = [
        TestingQuestionInline,
        TestingPassageInline,
    ]
    date_hierarchy = 'date_added'
    fieldsets = [
        [
            TestingSuit._meta.verbose_name, {
                'fields': ['name', 'account', 'picture', 'duration', 'complexity', 'description'],
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(TestingSuitAdmin, self).get_queryset(request)
        qs = qs.annotate(count_questions=Count('questions', distinct=True))
        return qs

    def get_count_questions(self, obj):
        return obj.count_questions
    get_count_questions.admin_order_field = 'count_questions'
    get_count_questions.short_description = _('Count questions')


class TestingPassageAdmin(admin.ModelAdmin):
    """

    """

    list_display = ['testing_suit', 'account', 'status', 'scope', 'date_passage']
    date_hierarchy = 'date_passage'
    list_filter = [
        ('testing_suit', admin.RelatedOnlyFieldListFilter),
        ('account', admin.RelatedOnlyFieldListFilter),
        'status',
        'date_passage',
    ]
    fieldsets = [
        [
            TestingPassage._meta.verbose_name, {
                'fields': ['testing_suit', 'account', 'status', 'scope'],
            }
        ]
    ]
    readonly_fields = ['testing_suit', 'account', 'status', 'scope']


class TestingVariantInline(admin.TabularInline):
    """
    Tabular Inline View for TestingVariant
    """

    model = TestingVariant
    min_num = 3
    max_num = 6
    extra = 1
    fk_name = 'question'
    formset = TestingVariantInlineFormSet


class TestingQuestionAdmin(admin.ModelAdmin):
    """
    Admin View for TestingQuestion
    """

    search_fields = ('title',)
    list_display = ('cropped_title', 'testing_suit', 'is_new', 'get_count_variants', 'date_modified', 'date_added')
    list_filter = (
        'date_modified',
        'date_added',
        ('testing_suit', admin.RelatedOnlyFieldListFilter),
    )
    inlines = [
        TestingVariantInline,
    ]
    date_hierarchy = 'date_added'
    fieldsets = [
        [
            TestingQuestion._meta.verbose_name, {
                'fields': ['title', 'testing_suit', 'text_question'],
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(TestingQuestionAdmin, self).get_queryset(request)
        qs = qs.annotate(count_variants=Count('variants', distinct=True))
        return qs

    def get_count_variants(self, obj):
        return obj.count_variants
    get_count_variants.admin_order_field = 'count_variants'
    get_count_variants.short_description = _('Count variants')


class TestingVariantAdmin(admin.ModelAdmin):
    '''
        Admin View for TestingVariant
    '''
    list_display = ('cropped_text_variant', 'question', 'is_right_variant')
    list_filter = (
        ('question', admin.RelatedOnlyFieldListFilter),
        ('is_right_variant', admin.BooleanFieldListFilter),
    )
    search_fields = ('question__title',)
    fieldsets = [
        [
            TestingVariant._meta.verbose_name, {
                'fields': ['question', 'text_variant', 'is_right_variant'],
            }
        ]
    ]
