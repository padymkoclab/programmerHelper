
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.app_generic_models.admin import OpinionGenericInline, CommentGenericInline

from .models import Course, Lesson, Sublesson


class LessonInline(admin.StackedInline):
    '''
    Stacked Inline View for Lesson
    '''

    model = Lesson
    min_num = Course.MIN_COUNT_LESSONS
    max_num = Course.MAX_COUNT_LESSONS
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    '''
    Admin View for Course
    '''

    list_display = (
        'name',
        'picture',
        'lexer',
        'get_generalized_scope',
        'get_count_lessons',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('lexer', admin.AllValuesFieldListFilter),
        'date_added',
        'date_modified',
    )
    inlines = [
        LessonInline,
    ]
    search_fields = ('name',)
    fields = ['name', 'picture', 'description', 'lexer', 'authorship']
    date_hierarchy = 'date_added'
    filter_horizontal = ['authorship']

    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_lessons=Count('lessons', distinct=True),
        )
        return qs

    def get_count_lessons(self, obj):
        return obj.count_lessons
    get_count_lessons.admin_order_field = 'count_lessons'
    get_count_lessons.short_description = _('Count lessons')


class SublessonInline(admin.StackedInline):
    '''
    Stacked Inline View for Sublesson
    '''

    model = Sublesson
    min_num = Lesson.MIN_COUNT_SUBLESSONS
    max_num = Lesson.MAX_COUNT_SUBLESSONS
    extra = 0


class LessonAdmin(admin.ModelAdmin):
    '''
    Admin View for Lesson
    '''

    list_display = (
        'name',
        'course',
        'number',
        'is_completed',
        'get_count_opinions',
        'get_count_comments',
        'get_scope',
        'views',
        'get_count_sublessons',
        'date_modified',
        'date_added',
    )
    list_filter = ('date_modified',)
    inlines = [
        OpinionGenericInline,
        SublessonInline,
        CommentGenericInline,
    ]
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super(LessonAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_sublessons=Count('sublessons', distinct=True),
            count_comments=Count('comments', distinct=True),
            count_opinions=Count('opinions', distinct=True),
        )
        return qs

    def get_count_sublessons(self, obj):
        return obj.count_sublessons
    get_count_sublessons.admin_order_field = 'count_sublessons'
    get_count_sublessons.short_description = _('Count sublessons')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')


class SublessonAdmin(admin.ModelAdmin):
    '''
    Admin View for Sublesson
    '''

    list_display = ('title', 'lesson', 'number', 'is_new', 'date_modified', 'date_added')
    list_filter = ('lesson', 'date_modified', 'date_added')
    search_fields = ('title', 'lesson__name')
    date_hierarchy = 'date_modified'
    fields = ('title', 'lesson', 'number', 'text', 'code')
