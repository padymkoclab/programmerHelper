
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import ForumSection, ForumTopic, ForumPost


class ForumTopicInline(admin.StackedInline):
    '''
        Tabular Inline View for ForumTopic
    '''

    model = ForumTopic
    min_num = 1
    extra = 0
    fk_name = 'theme'


class ForumSectionAdmin(admin.ModelAdmin):
    '''
    Admin View for ForumSection
    '''

    list_display = (
        'name',
        'get_count_topics',
        'get_count_posts',
        'count_active_users',
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
    fieldsets = [
        [
            ForumSection._meta.verbose_name, {
                'fields': ['name', 'description']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(ForumSectionAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_topics=Count('topics', distinct=True),
            count_posts=Count('topics__posts', distinct=True),
        )
        return qs

    def get_count_topics(self, obj):
        return obj.topics.count()
    get_count_topics.admin_order_field = 'count_topics'
    get_count_topics.short_description = _('Count topics')


class ForumPostInline(admin.StackedInline):
    '''
        Tabular Inline View for ForumPost
    '''

    model = ForumPost
    min_num = 1
    extra = 0
    fk_name = 'topic'


class ForumTopicAdmin(admin.ModelAdmin):
    '''
    Admin View for ForumTopic
    '''

    list_display = (
        'name',
        'theme',
        'author',
        'get_count_posts',
        'count_active_users',
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
    fieldsets = [
        [
            ForumTopic._meta.verbose_name, {
                'fields': ['name', 'theme', 'author', 'status', 'description']
            }
        ]
    ]
    search_fields = ['name']

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

    list_display = ('topic', 'author', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('topic', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    search_fields = ['content']
    fieldsets = [
        [
            ForumPost._meta.verbose_name, {
                'fields': ['topic', 'author', 'content']
            }
        ]
    ]
