
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.core.admin import AdminSite, AppAdmin

from .models import Section, Forum, Topic, Post
from .forms import SectionAdminModelForm


@admin.register(Section, site=AdminSite)
class SectionAdmin(admin.ModelAdmin):

    form = SectionAdminModelForm
    list_display = (
        'name',
        'get_count_forums',
        'position',
    )
    search_fields = ('name', )


class TopicInline(admin.StackedInline):
    '''
        Tabular Inline View for Topic
    '''

    model = Topic
    min_num = 1
    extra = 0
    fk_name = 'forum'


@admin.register(Forum, site=AdminSite)
class ForumAdmin(admin.ModelAdmin):
    '''
    Admin View for Forum
    '''

    list_display = (
        'name',
        'get_count_topics',
        'get_total_count_posts',
        'count_active_users',
        'date_modified',
    )
    list_filter = (
        'date_modified',
    )
    search_fields = ('name',)
    inlines = [
        TopicInline,
    ]
    fieldsets = [
        [
            Forum._meta.verbose_name, {
                'fields': ['name', 'description']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(ForumAdmin, self).get_queryset(request)
        qs = qs.forum_with_all_annotated_fields()
        return qs


# class PostInline(admin.StackedInline):
#     '''
#         Tabular Inline View for Post
#     '''

#     model = Post
#     min_num = 1
#     extra = 0
#     fk_name = 'topic'


# class TopicAdmin(admin.ModelAdmin):
#     '''
#     Admin View for Topic
#     '''

#     list_display = (
#         'name',
#         'theme',
#         'author',
#         'get_count_posts',
#         'count_active_users',
#         'status',
#         'is_new',
#         'date_modified',
#         'date_added',
#     )
#     list_filter = (
#         ('author', admin.RelatedOnlyFieldListFilter),
#         ('theme', admin.RelatedOnlyFieldListFilter),
#         'status',
#         'date_modified',
#         'date_added',
#     )
#     date_hierarchy = 'date_added'
#     inlines = [
#         PostInline,
#     ]
#     fieldsets = [
#         [
#             Topic._meta.verbose_name, {
#                 'fields': ['name', 'theme', 'author', 'status', 'description']
#             }
#         ]
#     ]
#     search_fields = ['name']

#     def get_queryset(self, request):
#         qs = super(TopicAdmin, self).get_queryset(request)
#         qs = qs.annotate(
#             count_posts=Count('posts', distinct=True),
#         )
#         return qs

#     def get_count_posts(self, obj):
#         return obj.count_posts
#     get_count_posts.admin_order_field = 'count_posts'
#     get_count_posts.short_description = _('Count posts')


# class PostAdmin(admin.ModelAdmin):
#     '''
#     Admin View for Post
#     '''

#     list_display = ('topic', 'author', 'is_new', 'date_modified', 'date_added')
#     list_filter = (
#         ('author', admin.RelatedOnlyFieldListFilter),
#         ('topic', admin.RelatedOnlyFieldListFilter),
#         'date_modified',
#         'date_added',
#     )
#     date_hierarchy = 'date_added'
#     search_fields = ['content']
#     fieldsets = [
#         [
#             Post._meta.verbose_name, {
#                 'fields': ['topic', 'author', 'content']
#             }
#         ]
#     ]
