
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Count

from .forms import SolutionForm, QuestionForm
from .models import Answer, SolutionComment, Solution, OpinionAboutAnswer, AnswerComment, Question


class SolutionInline(admin.StackedInline):
    '''
    Tabular Inline View for Solution
    '''

    # inline Opinions
    model = Solution
    extra = 1
    fk_name = 'category'
    fieldsets = [
        [None, {
            'fields': ['title', 'body', 'tags', 'useful_links']
        }]
    ]
    filter_vertical = ['useful_links']
    filter_horizontal = ['tags']


class SolutionCategoryAdmin(admin.ModelAdmin):
    """
    Admin View for SolutionCategory
    """

    list_display = ('name', 'lexer', 'get_count_solutions', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('lexer', admin.AllValuesFieldListFilter),
        'date_modified',
        'date_added',
    )
    # list_editable = ['lexer']
    date_hierarchy = 'date_added'
    search_fields = ('name',)
    inlines = [
        SolutionInline,
    ]

    def get_queryset(self, request):
        qs = super(SolutionCategoryAdmin, self).get_queryset(request)
        qs = qs.annotate(count_solutions=Count('solutions'))
        return qs

    def get_count_solutions(self, obj):
        return obj.count_solutions
    get_count_solutions.short_description = _('Count solutions')
    get_count_solutions.admin_order_field = 'count_solutions'


class SolutionCommentInline(admin.StackedInline):
    '''
        Tabular Inline View for SolutionComment
    '''

    model = SolutionComment
    extra = 1
    fk_name = 'solution'
    fields = ['author', 'text_comment']
    verbose_name = _('Comment')
    verbose_name_plural = _('Comments')


class OpinionAboutSolutionInline(admin.TabularInline):
    '''
    Tabular Inline View for A
    '''

    model = Solution.opinions.through
    extra = 1
    fields = ['user', 'is_useful', 'is_favorite']


class SolutionAdmin(admin.ModelAdmin):
    """
    Admin View for Solution
    """

    list_display = (
        'title',
        'category',
        'get_count_useful_links',
        'get_count_good_opinions',
        'get_count_bad_opinions',
        'get_count_favorites',
        'get_count_opinions',
        'get_count_comments',
        'get_count_tags',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        'date_modified',
        'date_added',
        ('category', admin.RelatedFieldListFilter),
    )
    search_fields = ('title',)
    date_hierarchy = 'date_added'
    inlines = [
        OpinionAboutSolutionInline,
        SolutionCommentInline,
    ]
    fields = ['title', 'category', 'body', 'useful_links', 'tags']
    filter_horizontal = ['tags']
    filter_vertical = ['useful_links']
    form = SolutionForm

    def get_queryset(self, request):
        qs = super(SolutionAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_useful_links=Count('useful_links', distinct=True),
            count_opinions=Count('opinions', distinct=True),
            count_comments=Count('comments', distinct=True),
            count_tags=Count('tags', distinct=True),
        )
        return qs

    def get_count_useful_links(self, obj):
        return obj.count_useful_links
    get_count_useful_links.short_description = _('Count links')
    get_count_useful_links.admin_order_field = 'count_useful_links'

    def get_count_good_opinions(self, obj):
        return obj.opinions.through.objects.filter(solution=obj, is_useful=True).count()
    get_count_good_opinions.short_description = _('Count good opinions')

    def get_count_bad_opinions(self, obj):
        return obj.opinions.through.objects.filter(solution=obj, is_useful=False).count()
    get_count_bad_opinions.short_description = _('Count bad opinions')

    def get_count_favorites(self, obj):
        return obj.opinions.through.objects.filter(solution=obj, is_favorite=obj.opinions.through.YES).count()
    get_count_favorites.short_description = _('Count favorites')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.short_description = _('Total count opinions')
    get_count_opinions.admin_order_field = 'count_opinions'

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.short_description = _('Count comments')
    get_count_comments.admin_order_field = 'count_comments'

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')


class OpinionAboutSolutionAdmin(admin.ModelAdmin):
    '''
        Admin View for OpinionAboutSolution
    '''

    list_display = ('user', 'solution', 'is_useful', 'is_favorite', 'date_modified')
    list_filter = (
        ('user', admin.RelatedFieldListFilter),
        ('solution', admin.RelatedFieldListFilter),
        'is_useful',
        'is_favorite',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    fields = ['solution', 'user', 'is_useful', 'is_favorite']


class SolutionCommentAdmin(admin.ModelAdmin):
    '''
        Admin View for SolutionComment
    '''
    list_display = ('author', 'solution', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        'date_modified',
        'date_added',
        ('author', admin.RelatedFieldListFilter),
        ('solution', admin.RelatedFieldListFilter),
    )
    date_hierarchy = 'date_added'
    fields = ['solution', 'author', 'text_comment']


class AnswerInline(admin.StackedInline):
    '''
    Stacked Inline View for Answer
    '''

    model = Answer
    extra = 1
    fk_name = 'question'
    fields = ['author', 'is_acceptable', 'text_answer']


class OpinionAboutQuestionInline(admin.TabularInline):
    '''
    Tabular Inline View for A
    '''

    model = Question.opinions.through
    extra = 1
    fields = ['user', 'is_useful', 'is_favorite']


class QuestionAdmin(admin.ModelAdmin):
    '''
    Admin View for Question
    '''

    list_display = (
        'title',
        'author',
        'status',
        'get_count_answers',
        'get_count_good_opinions',
        'get_count_bad_opinions',
        'get_count_favorites',
        'get_count_opinions',
        'get_count_tags',
        'is_dublicated',
        'is_new',
        'date_modified',
        'date_added')
    list_filter = (
        ('author', admin.RelatedFieldListFilter),
        'status',
        'date_modified',
        'date_added',
        'is_dublicated',
    )
    inlines = [
        OpinionAboutQuestionInline,
        AnswerInline,
    ]
    fields = ['title', 'author', 'status', 'text_question', 'is_dublicated', 'tags']
    filter_horizontal = ['tags']
    form = QuestionForm

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_answers=Count('answers', distinct=True),
            count_tags=Count('tags', distinct=True),
            count_opinions=Count('opinions', distinct=True),
        )
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

    def get_count_good_opinions(self, obj):
        return obj.opinions.through.objects.filter(question=obj, is_useful=True).count()
    get_count_good_opinions.short_description = _('Count good opinions')

    def get_count_bad_opinions(self, obj):
        return obj.opinions.through.objects.filter(question=obj, is_useful=False).count()
    get_count_bad_opinions.short_description = _('Count bad opinions')

    def get_count_favorites(self, obj):
        return obj.opinions.through.objects.filter(question=obj, is_favorite=obj.opinions.through.YES).count()
    get_count_favorites.short_description = _('Count favorites')


class OpinionAboutQuestionAdmin(admin.ModelAdmin):
    """

    """

    list_display = ['question', 'user', 'is_useful', 'is_favorite', 'date_modified']
    fields = ['question', 'user', 'is_useful', 'is_favorite']
    list_filter = [
        ('question', admin.RelatedFieldListFilter),
        ('user', admin.RelatedFieldListFilter),
        'is_useful',
        'is_favorite',
        'date_modified',
    ]
    date_hierarchy = 'date_modified'


class OpinionAboutAnswerInline(admin.TabularInline):
    '''
    Tabular Inline View for OpinionAboutAnswer
    '''

    model = OpinionAboutAnswer
    extra = 1
    fk = 'opinions'


class AnswerCommentInline(admin.StackedInline):
    '''
    Tabular Inline View for AnswerComment
    '''

    model = AnswerComment
    extra = 1
    fk = 'answer'
    fields = ['author', 'text_comment']
    verbose_name = _('Comment')


class AnswerAdmin(admin.ModelAdmin):
    '''
        Admin View for Answer
    '''

    list_display = (
        'question',
        'author',
        'is_acceptable',
        'get_count_comments',
        'get_count_positive_votes',
        'get_count_negative_votes',
        'get_count_opinions',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('author', admin.RelatedFieldListFilter),
        ('question', admin.RelatedFieldListFilter),
        'opinions',
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    inlines = [
        AnswerCommentInline,
        OpinionAboutAnswerInline,
    ]
    fields = ['question', 'author', 'text_answer', 'is_acceptable']

    def get_queryset(self, request):
        qs = super(AnswerAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_opinions=Count('opinions', distinct=True),
            count_comments=Count('comments', distinct=True),
        )
        return qs

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count voted opinions')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def get_count_positive_votes(self, obj):
        return OpinionAboutAnswer.objects.filter(answer=obj, liked_this_answer=True).count()
        # return obj.count_opinions
    # get_count_opinions.admin_order_field = 'count_opinions'
    get_count_positive_votes.short_description = _('Count positive votes')

    def get_count_negative_votes(self, obj):
        return OpinionAboutAnswer.objects.filter(answer=obj, liked_this_answer=False).count()
    # get_count_opinions.admin_order_field = 'count_opinions'
    get_count_negative_votes.short_description = _('Count negative votes')


class AnswerCommentAdmin(admin.ModelAdmin):
    '''
        Admin View for CommentAnswer
    '''
    list_display = ('answer', 'author', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('answer', admin.RelatedFieldListFilter),
        ('author', admin.RelatedFieldListFilter),
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    fields = ['answer', 'author', 'text_comment']
