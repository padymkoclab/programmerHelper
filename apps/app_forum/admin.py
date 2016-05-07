
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import ForumTopic, ForumPost


class ForumTopicInline(admin.StackedInline):
    '''
        Tabular Inline View for ForumTopic
    '''

    model = ForumTopic
    min_num = 0
    extra = 1
    fk_name = 'theme'


class ForumPostInline(admin.StackedInline):
    '''
        Tabular Inline View for ForumPost
    '''

    model = ForumPost
    min_num = 0
    extra = 1
    fk_name = 'topic'


class ForumThemeAdmin(admin.ModelAdmin):
    '''
    Admin View for ForumTheme
    '''

    list_display = (
        'name',
        'get_count_topic',
        'get_count_total_posts',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        'date_modified',
        'date_added',
    )
    search_fields = ('name',)
    inlines = [
        ForumTopicInline,
    ]

    def get_queryset(self, request):
        qs = super(ForumThemeAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_topics=Count('topics', distinct=True),
            count_posts=Count('topics__posts', distinct=True),
        )
        return qs

    def get_count_topic(self, obj):
        return obj.count_topics
    get_count_topic.admin_order_field = 'count_topics'
    get_count_topic.short_description = _('Count topics')

    def get_count_total_posts(self, obj):
        return obj.count_posts
    get_count_total_posts.admin_order_field = 'count_posts'
    get_count_total_posts.short_description = _('Count total posts')


class ForumTopicAdmin(admin.ModelAdmin):
    '''
    Admin View for ForumTopic
    '''

    list_display = (
        'name',
        'theme',
        'author',
        'get_count_posts',
        'status',
        'status_changed',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('theme', admin.RelatedOnlyFieldListFilter),
        'status',
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    inlines = [
        ForumPostInline,
    ]

    def get_queryset(self, request):
        qs = super(ForumTopicAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_posts=Count('posts', distinct=True),
        )
        return qs

    def get_count_posts(self, obj):
        return obj.count_posts
    get_count_posts.admin_order_field = 'count_posts'
    get_count_posts.short_description = _('Count posts')


class ForumPostAdmin(admin.ModelAdmin):
    '''
    Admin View for ForumPost
    '''

    list_display = ('author', 'topic', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('topic', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
