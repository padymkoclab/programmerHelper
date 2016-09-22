
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

from apps.polls.listfilters import IsActiveVoterListFilter
from apps.diaries.admin import DiaryInline

from .actions import (
    make_users_as_non_superuser,
    make_users_as_superuser,
    make_users_as_non_active,
    make_users_as_active,
)
from .forms import UserChangeForm, UserCreationForm, LevelAdminModelForm
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


inlines = [
    ProfileInline, DiaryInline
]
for model in [
    Snippet, Article, Solution, Question, Answer,
    Comment, Reply, Opinion, Mark, Flavour, Topic, Post,
    # Vote,
]:

    class ObjectInlineFormSet(forms.BaseInlineFormSet):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # make slice form in formsets
            self.queryset = self.queryset.order_by('-date_added')[:3]

    def truncated_str(self, obj):
        return truncatechars(force_text(obj), 120)
    truncated_str.short_description = model._meta.verbose_name

    ObjectInline = type('ObjectInline', (admin.TabularInline, ), dict(
        model=model,
        fields=('truncated_str', 'date_added'),
        readonly_fields=('truncated_str', 'date_added'),
        can_delete=False,
        max_num=0,
        extra=0,
        show_change_link=True,
        suit_classes='suit-tab suit-tab-objects',
        formset=ObjectInlineFormSet,
        truncated_str=truncated_str,
    ))

    inlines.append(ObjectInline)


@admin.register(User, site=AdminSite)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for model User
    """

    form = UserChangeForm
    add_form = UserCreationForm
    actions = [make_users_as_non_superuser, make_users_as_superuser, make_users_as_non_active, make_users_as_active]

    # set it value in empty, since it should be change in following views
    list_display = (
        'display_name',
        'username',
        'email',
        'level',
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

    search_fields = ('display_name', 'email', 'username')
    date_hierarchy = 'date_joined'

    filter_horizontal = ['groups']
    filter_vertical = ['user_permissions']
    add_fieldsets = [
        (
            None, {
                'fields': [
                    'email',
                    'username',
                    'password1',
                    'password2',
                ]
            }
        )
    ]
    readonly_fields = (
        'display_avatar',
        'last_login',
        'reputation',
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
        'display_diary_details',
    )

    suit_form_tabs = [
        ('general', _('General')),
        ('permissions', _('Permissions')),
        ('groups', _('Groups')),
        ('profile', _('Profile')),
        ('diary', _('Diary')),
        ('objects', _('Objects')),
        ('tags', _('Tags')),
        ('badges', _('Badges')),
        ('activity', _('Activity')),
        ('notifications', _('Notifications')),
        ('summary', _('Summary')),
    ]

    def get_queryset(self, request):

        qs = super(UserAdmin, self).get_queryset(request)

        # if request.path == '/admin/users/user/voters/':
        #     qs = qs.model.polls.users_as_voters()
        #     return qs.filter(count_votes__gt=0)

        qs = qs.annotate()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                None, {
                    'classes': ('suit-tab suit-tab-general', ),
                    'fields': (
                        'display_name',
                        'email',
                        'username',
                        'password',
                        'is_active',
                        'is_superuser',
                        'display_avatar',
                    )
                },
            ),
        ]

        if obj is not None:
            fieldsets.extend((

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
                            'reputation',
                            'last_seen',
                            'last_login',
                            'date_joined',
                            'display_diary_details',
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
            ))

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            return [inline(self.model, self.admin_site) for inline in inlines]
        return ()

    def get_urls(self):

        urls = super(UserAdmin, self).get_urls()

        additional_urls = [
            url(r'voters/$', self.voters_view, {}, 'users_user_voters'),
        ]

        # additional urls must be before standartic urls
        urls = additional_urls + urls

        return urls

    def change_view(self, request, object_id, form_url='', extra_context=None):

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

    pass


class UserInline(admin.TabularInline):

    model = User
    fields = ('display_admin_change_link', 'reputation', 'date_joined')
    readonly_fields = ('display_admin_change_link', 'reputation', 'date_joined')
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
