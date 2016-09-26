
import logging

from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.db import models
from django.template.defaultfilters import truncatechars
from django import forms
from django.utils.text import force_text
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.core.admin import AdminSite

from apps.snippets.models import Snippet
from apps.articles.models import Article
from apps.solutions.models import Solution
from apps.questions.models import Question, Answer
from apps.comments.models import Comment
from apps.replies.models import Reply
from apps.flavours.models import Flavour
from apps.opinions.models import Opinion
from apps.marks.models import Mark
from apps.polls.models import Vote
from apps.forums.models import Topic, Post
from apps.testing.models import Passage

from apps.polls.listfilters import IsActiveVoterListFilter

from .actions import (
    make_users_as_non_superuser,
    make_users_as_superuser,
    make_users_as_non_active,
    make_users_as_active,
)
from .forms import UserChangeForm, UserCreateAdminModelForm, LevelAdminModelForm, ProfileAdminModelForm
from .models import User, Level, Profile
from .listfilters import ListFilterLastLogin


logger = logging.getLogger('django.development')


class ProfileInline(admin.StackedInline):

    template = 'users/admin/edit_inline/stacked_OneToOne.html'
    model = Profile
    fields = (
        'views',
        'about',
        'signature',
        'presents_on_gmail',
        'presents_on_github',
        'presents_on_stackoverflow',
        'personal_website',
        'gender',
        'job',
        'location',
        'latitude',
        'longitude',
        'phone',
        'date_birthday',
        'real_name',
    )
    readonly_fields = (
        'views',
        'about',
        'signature',
        'presents_on_gmail',
        'presents_on_github',
        'presents_on_stackoverflow',
        'personal_website',
        'gender',
        'job',
        'location',
        'latitude',
        'longitude',
        'phone',
        'date_birthday',
        'real_name',
    )
    show_change_link = True
    verbose_name_plural = ''

    suit_classes = 'suit-tab suit-tab-profile'


inlines = []
for model in [
    Snippet, Article, Solution, Question, Answer,
    Comment, Reply, Opinion, Mark, Flavour, Topic, Post,
    Vote, Passage
]:

    class ObjectInlineFormSet(forms.BaseInlineFormSet):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # make slice form in formsets
            self.queryset = self.queryset.order_by('-created')[:3]

    def truncated_str(self, obj):
        return truncatechars(force_text(obj), 120)
    truncated_str.short_description = model._meta.verbose_name

    def get_fields(self, request, obj=None):
        return ('truncated_str', 'created'),

    ObjectInline = type('ObjectInline', (admin.TabularInline, ), dict(
        model=model,
        readonly_fields=('truncated_str', 'created'),
        can_delete=False,
        template='users/admin/edit_inline/tabular_tab_activity.html',
        max_num=0,
        extra=0,
        show_change_link=True,
        suit_classes='suit-tab suit-tab-activity',
        formset=ObjectInlineFormSet,
        truncated_str=truncated_str,
        get_fields=get_fields,
    ))

    inlines.append(ObjectInline)


@admin.register(User, site=AdminSite)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for model User
    """

    form = UserChangeForm
    add_form = UserCreateAdminModelForm
    actions = (
        make_users_as_non_superuser,
        make_users_as_superuser,
        make_users_as_non_active,
        make_users_as_active,
    )

    # set it value in empty, since it should be change in following views
    list_display = (
        'alias',
        'username',
        'email',
        'level',
        'reputation',
        'is_active',
        'is_superuser',
        'last_login',
        'date_joined',
    )
    list_filter = [
        ('level', admin.RelatedOnlyFieldListFilter),
        ('is_active', admin.BooleanFieldListFilter),
        ('is_superuser', admin.BooleanFieldListFilter),
        ListFilterLastLogin,
        ('date_joined', admin.DateFieldListFilter),
    ]
    ordering = ('date_joined', )

    search_fields = ('alias', 'email', 'username')
    date_hierarchy = 'date_joined'

    filter_horizontal = ['groups']
    filter_vertical = ['user_permissions']
    add_fieldsets = (
        (
            None, {
                'fields': (
                    'email',
                    'username',
                    'alias',
                    'password1',
                    'password2',
                )
            }
        ),
    )
    readonly_fields = (
        'display_avatar',
        'last_login',
        # 'reputation',
        'level',
        'last_seen',
        'date_joined',
        'get_count_comments',
        'get_count_opinions',
        'get_count_likes',
        'get_count_marks',
        'get_count_questions',
        'get_count_snippets',
        'get_count_articles',
        'get_count_answers',
        'get_count_solutions',
        'get_count_posts',
        'get_count_topics',
        'get_count_test_suits',
        'get_count_passages',
        'get_count_votes',
        # 'display_diary_details',
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        # if request.path == '/admin/users/user/voters/':
        #     qs = qs.model.polls.users_as_voters()
        #     return qs.filter(count_votes__gt=0)

        qs = qs.annotate()
        return qs

    def get_fieldsets(self, request, obj=None):

        if obj is None:
            self.suit_form_tabs = ()
            self.suit_form_includes = ()
            return self.add_fieldsets

        else:

            self.suit_form_tabs = (
                ('general', _('General')),
                ('permissions', _('Permissions')),
                ('groups', _('Groups')),
                ('tags', _('Tags')),
                ('badges', _('Badges')),
                ('activity', _('Activity')),
                ('notifications', _('Notifications')),
                ('summary', _('Summary')),
            )

            self.suit_form_includes = (
                ('users/admin/user_admin_tab_tags.html', 'top', 'tags'),
            )

            return (
                (
                    None, {
                        'classes': ('suit-tab suit-tab-general', ),
                        'fields': (
                            'alias',
                            'email',
                            'username',
                            'password',
                            'is_active',
                            'is_superuser',
                            'display_avatar',
                        )
                    },
                ),
                (
                    None, {
                        'classes': ('suit-tab suit-tab-permissions', ),
                        'fields': (
                            'user_permissions',
                        )
                    }
                ),
                (
                    None, {
                        'classes': ('suit-tab suit-tab-groups', ),
                        'fields': (
                            'groups',
                        )
                    }
                ),
                (
                    None, {
                        'classes': ('suit-tab suit-tab-summary', ),
                        'fields': (
                            'level',
                            # 'reputation',
                            'last_seen',
                            'last_login',
                            'date_joined',
                            # 'display_diary_details',
                            'get_count_comments',
                            'get_count_opinions',
                            'get_count_likes',
                            'get_count_marks',
                            'get_count_questions',
                            'get_count_snippets',
                            'get_count_articles',
                            'get_count_answers',
                            'get_count_solutions',
                            'get_count_posts',
                            'get_count_topics',
                            'get_count_test_suits',
                            'get_count_passages',
                            'get_count_votes',
                        )
                    }
                ),
            )

    def get_urls(self):

        urls = super(UserAdmin, self).get_urls()

        additional_urls = [
            url(r'voters/$', self.voters_view, {}, 'users_user_voters'),
        ]

        # additional urls must be before standartic urls
        urls = additional_urls + urls

        return urls

    def change_view(self, request, object_id, form_url='', extra_context=None):

        if extra_context is None:
            extra_context = {}

        statistics_usage_tags = self.model.objects.get(pk=object_id).get_statistics_usage_tags(20)

        extra_context['statistics_usage_tags'] = statistics_usage_tags

        # for reject unneccessary calculation use straight access instead user.get_top_tag()
        extra_context['user_top_tag'] = None if statistics_usage_tags is not None else statistics_usage_tags[0][0]

        return super().change_view(request, object_id, form_url, extra_context)

    # def changelist_view(self, request, extra_context=None):

    #     # temproraly make a request.GET as a mutable object
    #     request.GET._mutable = True

    #     # get a custom value from a URL, if presents.
    #     # and keep this value on a instance of this class
    #     try:
    #         self.display_users = request.GET.pop('display_users')[0]
    #     except KeyError:
    #         self.display_users = None

    #     # restore the request.GET as a unmutable object
    #     request.GET._mutable = False

    #     if request.path == reverse('admin:users_user_changelist'):
    #         self.list_display = [
    #             'email',
    #             'username',
    #             'level',
    #             'is_active',
    #             'is_superuser',
    #             'last_login',
    #             'date_joined',
    #         ]
    #         self.list_filter = [
    #             ('level', LevelRelatedOnlyFieldListFilter),
    #             ('is_active', admin.BooleanFieldListFilter),
    #             ('is_superuser', admin.BooleanFieldListFilter),
    #             ListFilterLastLogin,
    #             ('date_joined', admin.DateFieldListFilter),
    #         ]
    #         self.ordering = ['date_joined']

    #     response = super(UserAdmin, self).changelist_view(request, extra_context)
    #     return response

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            # inlines = inlines
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def suit_cell_attributes(self, request, column):

        if column in ['date_joined', 'last_login']:
            css_class_align = 'right'
        elif column in ['alias', 'username', 'email']:
            css_class_align = 'left'
        else:
            css_class_align = 'center'

        return {'class': 'text-{}'.format(css_class_align)}

    def voters_view(self, request):
        """ """

        self.list_display = [
            'get_full_name',
            'get_count_votes',
            'is_active_voter',
            'get_date_latest_voting',
        ]

        self.list_filter = [
            IsActiveVoterListFilter,
            # ('date_latest_voting', admin.BooleanFieldListFilter),
        ]
        self.ordering = ['count_votes', 'date_latest_voting']

        return self.changelist_view(request)

    def display_diary_details(self, obj):

        has_diary = obj.has_diary()

        msg = _('User has not a diary')
        link_url = reverse('admin:diaries_diary_add')
        link_text = _('Create now')

        return format_html(
            '<span>{}</span><form action="{}"><button type="submit">{}</button></form>', msg, link_url, link_text)

        if has_diary is True:
            msg = _('User has a diary')
            link_url = '2'
            link_text = _('Change it')

        return format_html('<span>{}</span><a href="{}">{}</a>', msg, link_url, link_text)


@admin.register(Profile, site=AdminSite)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'get_user__get_full_name',
        'gender',
        'views',
        'last_seen',
        'get_percentage_filling',
        'updated',
    )
    readonly_fields = (
        'get_user__display_avatar',
        'get_user__get_full_name',
    )
    # search_fields = ('user', )
    date_hierarchy = 'updated'
    list_filter = (
        'gender',
        'updated',
    )

    form = ProfileAdminModelForm
    fieldsets = (
        (
            None, {
                'fields': (
                    'get_user__display_avatar',
                    # 'views',
                    'signature',
                    'presents_on_gmail',
                    'presents_on_github',
                    'presents_on_stackoverflow',
                    'personal_website',
                    'gender',
                    'job',
                    'location',
                    ('longitude', 'latitude'),
                    'date_birthday',
                    'real_name',
                    'phone',
                    # 'updated',
                ),
            }
        ),
        (
            None, {
                'classes': ('full-width', ),
                'fields': (
                    'about',
                )
            }
        )
    )

    def suit_cell_attributes(self, request, column):

        if column in ['updated', 'last_seen']:
            css_class_align = 'right'
        elif column in ['get_user__get_full_name', ]:
            css_class_align = 'left'
        else:
            css_class_align = 'center'

        return {'class': 'text-{}'.format(css_class_align)}

    def get_user__display_avatar(self, obj):
        return obj.user.display_avatar()
    get_user__display_avatar.short_description = _('Avatar')

    def get_user__get_full_name(self, obj):
        return obj.user.get_full_name()
    get_user__get_full_name.short_description = _('User')


class UserInline(admin.TabularInline):

    model = User
    # fields = ('display_admin_change_link', 'reputation', 'date_joined')
    # readonly_fields = ('display_admin_change_link', 'reputation', 'date_joined')
    max_num = 0
    extra = 0
    can_delete = False

    suit_classes = 'suit-tab suit-tab-users'


@admin.register(Level, site=AdminSite)
class LevelAdmin(admin.ModelAdmin):
    '''
    Admin View for Level
    '''

    form = LevelAdminModelForm
    list_display = (
        'name',
        'get_count_users',
        'display_color',
        'description',
    )
    search_fields = ('name',)
    fieldsets = (
        (
            Level._meta.verbose_name, {
                'fields': (
                    'name',
                    'color',
                    'description',
                ),
                'classes': ('suit-tab suit-tab-general', )
            },
        ),
    )
    inlines = [UserInline]

    suit_form_tabs = (
        ('general', _('General')),
        ('users', _('Users')),
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        qs = qs.levels_with_count_users()
        return qs

    def formfield_for_choice_field(self, db_field, request, **kwargs):

        if db_field.name == "name":
            logger.warning('Do exclude used choices')
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def suit_cell_attributes(self, request, column):

        css_class_align = 'left'
        if column == 'get_count_users':
            css_class_align = 'center'
        return {'class': 'text-{}'.format(css_class_align)}

    def display_color(self, obj):
        """ """

        return format_html(
            '<span style="background-color: {};">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;{}',
            obj.color, obj.color,
        )
    display_color.short_description = Level._meta.get_field('color').verbose_name
    display_color.admin_order_field = 'color'
