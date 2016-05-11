
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from .models import Tag


class SolutionInline(admin.TabularInline):
    '''
    Tabular Inline View for Solution
    '''

    model = Tag.solutions.through
    extra = 1
    verbose_name = _('Solution')
    verbose_name_plural = _('Solutions')


class SnippetInline(admin.TabularInline):
    '''
    Tabular Inline View for Solution
    '''

    model = Tag.snippets.through
    extra = 1
    verbose_name = _('Snippet')
    verbose_name_plural = _('Snippets')


class ArticleInline(admin.TabularInline):
    '''
    Tabular Inline View for Solution
    '''

    model = Tag.articles.through
    extra = 1
    verbose_name = _('Article')
    verbose_name_plural = _('Articles')


class QuestionInline(admin.TabularInline):
    '''
    Tabular Inline View for Solution
    '''

    model = Tag.questions.through
    extra = 1
    verbose_name = _('Question')
    verbose_name_plural = _('Questions')


class TagAdmin(admin.ModelAdmin):
    '''
        Admin View for Tag
    '''

    list_display = (
        'name',
        'get_count_solutions_presents',
        'get_count_questions_presents',
        'get_count_snippets_presents',
        'get_count_articles_presents',
        'get_total_count_usage',
        'is_new',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    # list_filter = (
    #     'date_modified',
    # )
    # range count ListFilter
    search_fields = ('name',)
    fieldsets = [
        [
            Tag._meta.verbose_name, {
                'fields': ['name']
            }
        ]
    ]
    inlines = [
        SolutionInline,
        SnippetInline,
        ArticleInline,
        QuestionInline,
    ]

    def get_queryset(self, request):
        qs = super(TagAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_solutions=Count('solutions', distinct=True),
            count_snippets=Count('snippets', distinct=True),
            count_questions=Count('questions', distinct=True),
            count_articles=Count('articles', distinct=True),
        )
        return qs

    def get_count_solutions_presents(self, obj):
        return obj.count_solutions
    get_count_solutions_presents.admin_order_field = 'count_solutions'
    get_count_solutions_presents.short_description = _('In how many solutions presents')

    def get_count_snippets_presents(self, obj):
        return obj.count_snippets
    get_count_snippets_presents.admin_order_field = 'count_snippets'
    get_count_snippets_presents.short_description = _('In how many snippets presents')

    def get_count_questions_presents(self, obj):
        return obj.count_questions
    get_count_questions_presents.admin_order_field = 'count_questions'
    get_count_questions_presents.short_description = _('In how many questions presents')

    def get_count_articles_presents(self, obj):
        return obj.count_articles
    get_count_articles_presents.admin_order_field = 'count_articles'
    get_count_articles_presents.short_description = _('In how many articles presents')

    def get_total_count_usage(self, obj):
        return \
            self.get_count_solutions_presents(obj) + self.get_count_snippets_presents(obj) + \
            self.get_count_questions_presents(obj) + self.get_count_articles_presents(obj)
    # get_total_count_usage.admin_order_field = 'count_articles'
    get_total_count_usage.short_description = _('Total count usage')
