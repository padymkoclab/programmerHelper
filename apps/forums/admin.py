
from django.template import Context, loader
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db import models

from utils.django.widgets import BooleanRadioSelect
from utils.django.datetime_utils import convert_date_to_django_date_format

# from apps.core.admin import AdminSite, AppAdmin

from .models import Section, Forum, Topic, Post
from .forms import SectionAdminModelForm
from .apps import ForumsConfig
from .forms import (
    FormAdminModelForm,
    ForumInlineAdminModelForm,
    TopicAdminModelForm,
    PostAdminModelForm,
)


# @AdminSite.register_app_admin_class
# class ThisAppAdmin(AppAdmin):
class ThisAppAdmin():

    label = ForumsConfig.label

    def get_context_for_tables_of_statistics(self):

        return (
            (_('Forums'), (
                (_('Count sections'), Section.objects.count()),
                (_('Count forums'), Forum.objects.count()),
                (_('Count topics'), Topic.objects.count()),
                (_('Count posts'), Post.objects.count()),
            )),
        )

    def get_context_for_charts_of_statistics(self):

        return (
            {
                'title': _('Chart count posts for the past year'),
                'table': {
                    'fields': ('Month, year', 'Count posts'),
                    'data': Post.objects.get_statistics_count_posts_for_the_past_year(),
                },
                'chart': Post.objects.get_chart_count_posts_for_the_past_year(),
            },
        )


class ForumInline(admin.TabularInline):

    form = ForumInlineAdminModelForm
    model = Forum
    extra = 0
    max_num = 0
    fk_name = 'section'
    can_delete = False
    readonly_fields = (
        'truncated_name_with_admin_url',
        'get_count_topics',
        'get_total_count_posts',
        'display_details_latest_post',
    )
    fields = (
        'truncated_name_with_admin_url',
        'get_count_topics',
        'get_total_count_posts',
        'display_details_latest_post',
    )

    suit_classes = 'suit-tab suit-tab-forums'

    def truncated_name_with_admin_url(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            obj.get_admin_url(),
            truncatechars(obj.name, 50),
        )
    truncated_name_with_admin_url.short_description = Forum._meta.get_field('name').verbose_name


# @admin.register(Section, site=AdminSite)
class SectionAdmin(admin.ModelAdmin):

    form = SectionAdminModelForm
    list_display = (
        'name',
        'position',
        'get_count_forums',
        'get_total_count_topics',
        'get_total_count_posts',
    )
    search_fields = ('name', )
    readonly_fields = (
        'get_count_forums',
    )
    filter_horizontal = ('groups', )

    suit_form_tabs = (
        ('general', _('General')),
        ('forums', _('Forums')),
        ('statistics', _('Statistics')),
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        qs = qs.sections_with_all_annotated_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (Section._meta.verbose_name, {
                'classes': ('suit-tab', 'suit-tab-general', ),
                'fields': (
                    'name',
                    'position',
                    'groups',
                ),
            }),
        ]

        if obj is not None:

            fieldsets.append(
                (_('Statistics'), {
                    'classes': ('suit-tab', 'suit-tab-statistics', ),
                    'fields': (
                        'get_count_forums',
                    )
                }),
            )

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            inlines = [ForumInline]
            return [inline(self.model, self.admin_site) for inline in inlines]

        return []

    def suit_cell_attributes(self, request, column):

        css_align = 'left' if column == 'name' else 'center'

        return {'class': 'text-{}'.format(css_align)}


class TopicInline(admin.TabularInline):
    '''
        Tabular Inline View for Topic
    '''

    model = Topic
    max_num = 0
    extra = 0
    can_delete = False
    fk_name = 'forum'
    fields = (
        'display_status',
        'display_topic',
        'views',
        'get_count_posts',
        'display_details_latest_post',
    )
    readonly_fields = (
        'display_status',
        'display_topic',
        'views',
        'get_count_posts',
        'display_details_latest_post'
    )

    suit_classes = 'suit-tab suit-tab-topics'

    def display_topic(self, obj):
        """ """

        return format_html(
            '<a href="{}">{}</a><br /><b>{}</b> >> {}',
            obj.get_admin_url(),
            truncatechars(obj.subject, 75),
            obj.user,
            convert_date_to_django_date_format(obj.created),
        )
    display_topic.short_description = _('Topic')

    def display_status(self, obj):
        """ """

        _template = loader.get_template('forums/admin/_topic_display_status.html')
        return _template.render(Context({'obj': obj}))
    display_status.short_description = _('Status')


# @admin.register(Forum, site=AdminSite)
class ForumAdmin(admin.ModelAdmin):
    '''
    Admin View for Forum
    '''

    form = FormAdminModelForm
    list_display = (
        'truncated_name',
        'get_count_topics',
        'get_total_count_posts',
        'get_count_active_users',
        'display_details_latest_post',
        'updated',
        'created',
    )
    list_filter = (
        'updated',
        'created',
    )
    search_fields = ('name',)
    readonly_fields = (
        'get_count_topics',
        'get_total_count_posts',
        'updated',
        'created',
    )
    filter_horizontal = ('moderators', )

    suit_form_tabs = (
        ('general', _('General')),
        ('topics', _('Topics')),
        ('statistics', _('Statistics')),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.forums_with_all_annotated_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                Forum._meta.verbose_name, {
                    'classes': ('suit-tab', 'suit-tab-general', ),
                    'fields': (
                        'name',
                        'slug',
                        'section',
                        'description',
                        'moderators',
                    )
                }
            ),
        ]

        if obj is not None:
            fieldsets.append(
                (
                    _('Statistics'), {
                        'classes': ('suit-tab', 'suit-tab-statistics', ),
                        'fields': (
                            'get_count_topics',
                            'get_total_count_posts',
                            'updated',
                            'created',
                        )
                    }
                ),
            )

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            inlines = [TopicInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def suit_cell_attributes(self, request, column):

        if column in ['created', 'updated']:
            css_align = 'right'
        elif column in ['truncated_name', 'display_details_latest_post']:
            css_align = 'left'
        else:
            css_align = 'center'

        return {'class': 'text-{}'.format(css_align)}

    def truncated_name(self, obj):

        return truncatechars(obj.name, 75)
    truncated_name.short_description = Forum._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'


class PostInline(admin.StackedInline):
    '''
        Tabular Inline View for Post
    '''

    form = PostAdminModelForm
    model = Post
    max_num = None
    extra = 0
    can_delete = True
    fk_name = 'topic'
    fields = ('user', 'markup', 'user_ip', 'content', 'display_content_html', 'created')
    readonly_fields = ('created', 'display_content_html')

    suit_classes = 'suit-tab suit-tab-posts'


# @admin.register(Topic, site=AdminSite)
class TopicAdmin(admin.ModelAdmin):
    '''
    Admin View for Topic
    '''

    formfield_overrides = {
        models.BooleanField: {'widget': BooleanRadioSelect},
    }
    prepopulated_fields = {'slug': ('subject', )}
    form = TopicAdminModelForm
    list_display = (
        'truncated_subject',
        'forum',
        'user',
        'get_count_posts',
        'count_active_users',
        'is_sticky',
        'is_opened',
        'is_new',
        'updated',
        'created',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'is_opened',
        'is_sticky',
        'updated',
        'created',
    )
    date_hierarchy = 'created'
    search_fields = ('subject', )
    readonly_fields = (
        'get_count_posts',
        'views',
        'updated',
        'created',
    )

    suit_form_tabs = (
        ('general', _('General')),
        ('posts', _('Posts')),
        ('statistics', _('Statistics')),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.topics_with_all_annotated_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                Topic._meta.verbose_name, {
                    'classes': ('suit-tab', 'suit-tab-general', ),
                    'fields': (
                        'subject',
                        'slug',
                        'forum',
                        'user',
                        'is_sticky',
                        'is_opened',
                    )
                }
            ),
        ]

        if obj is not None:
            fieldsets.append(
                (
                    _('Statistics'), {
                        'classes': ('suit-tab', 'suit-tab-statistics', ),
                        'fields': (
                            'get_count_posts',
                            'views',
                            'updated',
                            'created',
                        )
                    }
                ),
            )

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            inlines = [PostInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def suit_cell_attributes(self, request, column):

        if column in ['created', 'updated']:
            css_align = 'right'
        elif column in ['truncated_subject', 'display_details_latest_post']:
            css_align = 'left'
        else:
            css_align = 'center'

        return {'class': 'text-{}'.format(css_align)}

    def truncated_subject(self, obj):

        return truncatechars(obj.subject, 75)
    truncated_subject.short_description = Topic._meta.get_field('subject').verbose_name
    truncated_subject.admin_order_field = 'subject'


# @admin.register(Post, site=AdminSite)
class PostAdmin(admin.ModelAdmin):
    '''
    Admin View for Post
    '''

    form = PostAdminModelForm
    list_display = ('truncated_topic', 'user', 'markup', 'is_new', 'updated', 'created')
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('topic', admin.RelatedOnlyFieldListFilter),
        ('markup', admin.AllValuesFieldListFilter),
        'updated',
        'created',
    )
    date_hierarchy = 'created'
    search_fields = ('content', )
    readonly_fields = (
        'updated',
        'created',
        'display_content_html',
    )

    suit_form_tabs = (
        ('general', _('General')),
        ('statistics', _('Statistics')),
    )

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (Post._meta.verbose_name, {
                'classes': ('suit-tab', 'suit-tab-general', ),
                'fields': (
                    'topic',
                    'user',
                    'user_ip',
                    'markup',
                    'content',
                    'display_content_html',
                ),
            }),
        ]

        if obj is not None:

            fieldsets.append(
                (_('Statistics'), {
                    'classes': ('suit-tab', 'suit-tab-statistics', ),
                    'fields': (
                        'updated',
                        'created',
                    )
                }),
            )

        return fieldsets

    def suit_cell_attributes(self, request, column):

        if column == 'truncated_topic':
            css_align = 'left'
        elif column in ['created', 'updated']:
            css_align = 'right'
        else:
            css_align = 'center'

        return {'class': 'text-{}'.format(css_align)}

    def truncated_topic(self, obj):

        return truncatechars(obj.topic, 75)
    truncated_topic.short_description = Post._meta.get_field('topic').verbose_name
    truncated_topic.admin_order_field = 'topic'
