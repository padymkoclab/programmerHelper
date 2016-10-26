
import collections
import logging

from django.db.models.fields import BLANK_CHOICE_DASH
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.admin.site import DefaultSiteAdmin
from apps.admin.admin import ModelAdmin, StackedInline, TabularInline
from apps.admin.app import AppAdmin
from apps.polls.listfilters import IsActiveVoterListFilter

from .actions import (
    make_users_as_non_superuser,
    make_users_as_superuser,
    make_users_as_non_active,
    make_users_as_active,
)
from .constants import LEVELS
from .forms import UserChangeForm, UserCreateAdminModelForm, LevelAdminModelForm, ProfileAdminModelForm
from .models import User, Level, Profile
from .listfilters import ListFilterLastLogin
from .apps import UsersConfig


logger = logging.getLogger('django.development')


class UserAppAdmin(AppAdmin):

    app_config_class = UsersConfig
    app_icon = 'users'


class ProfileInline(StackedInline):

    template = 'users/admin/edit_inline/stacked_OneToOne.html'
    model = Profile
    fields = (
        'views',
        'about',
        'signature',
        'on_gmail',
        'on_github',
        'on_stackoverflow',
        'website',
        'gender',
        'job',
        # 'location',
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
        'on_gmail',
        'on_github',
        'on_stackoverflow',
        'website',
        'gender',
        'job',
        # 'location',
        'latitude',
        'longitude',
        'phone',
        'date_birthday',
        'real_name',
    )
    show_change_link = True
    verbose_name_plural = ''

    suit_classes = 'suit-tab suit-tab-profile'


# class UserAdmin(BaseUserAdmin):
class UserAdmin(ModelAdmin):
    """
    Admin configuration for model User
    """

    max_count_display_queryset = 3
    form = UserChangeForm
    add_form = UserCreateAdminModelForm
    actions = (
        make_users_as_non_superuser,
        make_users_as_superuser,
        make_users_as_non_active,
        make_users_as_active,
    )

    list_display = [
        ('users_main_info', {
            'title': _('Users (main information)'),
            'fields': (
                'alias',
                'username',
                'email',
                'is_active',
                'is_superuser',
                'date_joined',
            ),
        }),
        ('users_extra_info', {
            'title': _('Users (extra information)'),
            'fields': (
                'alias',
                'username',
                'email',
                'level',
                'reputation',
                'last_login',
            ),
        }),
        ('users_visits', {
            'title': _('Users and visits'),
            'fields': (
                'alias',
                'get_last_seen',
                'get_count_days_attendances',
            ),
        }),
        ('users_polls', {
            'title': _('Users and polls'),
            'fields': (
                '__str__',
                'get_count_votes',
                'is_active_voter',
                'get_date_latest_vote',
            ),
        }),
        ('users_questions', {
            'title': _('Users and questions'),
            'fields': (
                '__str__',
                'get_favorite_tags_of_questions',
                'get_count_questions',
                'get_total_rating_for_questions',
                'get_date_latest_question',
            ),
        }),
        ('users_answers', {
            'title': _('Users and answers'),
            'fields': (
                '__str__',
                'get_favorite_tags_of_answers',
                'get_count_answers',
                'get_total_rating_for_answers',
                'get_date_latest_answer',
            ),
        }),
        ('users_articles', {
            'title': _('Users and articles'),
            'fields': (
                '__str__',
                'get_favorite_tags_of_articles',
                'get_count_articles',
                'get_total_rating_for_articles',
                'get_date_latest_article',
            ),
        }),
        ('users_solutions', {
            'title': _('Users and solutions'),
            'fields': (
                '__str__',
                'get_favorite_tags_of_solutions',
                'get_count_solutions',
                'get_total_rating_for_solutions',
                'get_date_latest_solution',
            ),
        }),
        ('users_snippets', {
            'title': _('Users and snippets'),
            'fields': (
                '__str__',
                'get_favorite_tags_of_snippets',
                'get_count_snippets',
                'get_total_rating_for_snippets',
                'get_date_latest_snippet',
            ),
        }),
        ('users_comments', {
            'title': _('Users and comments'),
            'fields': (
                '__str__',
                'get_count_comments_of_articles',
                'get_count_comments_of_solutions',
                'get_count_comments_of_snippets',
                'get_count_comments_of_answers',
                'get_count_comments_of_utilities',
                'get_total_count_comments',
                'get_rating_comments',
                'get_date_latest_comment',
            ),
        }),

        # Library
        ('users_library', {
            'title': _('Users and library'),
            'fields': (
                '__str__',
                'get_count_replies',
                'get_date_latest_reply',
            ),
        }),

        # Opinions
        ('users_opinions', {
            'title': _('Users and opinions'),
            'fields': (
                '__str__',
                'get_count_opinions_of_solutions',
                'get_count_opinions_of_questions',
                'get_count_opinions_of_snippets',
                'get_count_opinions_of_utilities',
                'get_count_opinions_of_answers',
                'get_total_count_opinions',
                'get_date_latest_opinion',
            ),
        }),

        # Marks
        ('users_marks', {
            'title': _('Users and marks'),
            'fields': (
                '__str__',
                'get_count_marks',
                'get_date_latest_mark',
            ),
        }),

        # Badge
        ('users_badges', {
            'title': _('Users and badges'),
            'fields': (
                '__str__',
                'get_count_badges',
                'get_count_gold_badges',
                'get_count_silver_badges',
                'get_count_bronze_badges',
                'get_latest_badge',
                'get_date_getting_latest_badge',
            ),
        }),

        # Notification
        ('users_notifications', {
            'title': _('Users and notifications'),
            'fields': (
                '__str__',
                'get_count_notifications',
            ),
        }),

        # Forum
        ('users_forums', {
            'title': _('Users and forums'),
            'fields': (
                '__str__',
                'get_count_topics',
                'get_count_posts',
                'get_date_latest_activity_on_forums',
            ),
        }),

        # Tags
        ('users_tags', {
            'title': _('Users and tags '),
            'fields': (
                '__str__',
                'get_favorite_tags',
                'get_count_usaged_unique_tags',
                'get_total_count_usaged_tags',
            ),
        }),

    ]

    list_display_links = ('alias', )
    list_display_styles = (
        (
            ('__all__', ), {
                'align': 'center',
            }
        ),
        (
            ('date_joined', 'last_login'), {
                'align': 'right',
            }
        )
    )

    list_filter = [
        # ('level', admin.RelatedOnlyFieldListFilter),
        # ('is_active', admin.BooleanFieldListFilter),
        # ('is_superuser', admin.BooleanFieldListFilter),
        # ListFilterLastLogin,
        # ('date_joined', admin.DateFieldListFilter),
    ]
    ordering = ('date_joined', )
    list_per_page = 10
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

    def changelist_view(self, request, extra_context=None):

        # temproraly make a request.GET as a mutable object
        request.GET._mutable = True

        # get a custom value from a URL, if presents.
        # and keep this value on a instance of this class
        try:
            self.display_users = request.GET.pop('display_users')[0]
        except KeyError:
            self.display_users = None

        # restore the request.GET as a unmutable object
        request.GET._mutable = False

        if request.path == reverse('admin:users_user_changelist'):
            self.list_display = [
                'email',
                'username',
                'level',
                'is_active',
                'is_superuser',
                'last_login',
                'date_joined',
            ]
            self.list_filter = [
                # ('level', LevelRelatedOnlyFieldListFilter),
                ('is_active', admin.BooleanFieldListFilter),
                ('is_superuser', admin.BooleanFieldListFilter),
                ListFilterLastLogin,
                ('date_joined', admin.DateFieldListFilter),
            ]
            self.ordering = ['date_joined']

        response = super(UserAdmin, self).changelist_view(request, extra_context)
        return response

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            # inlines = inlines
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

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


class ProfileAdmin(ModelAdmin):

    list_display = (
        'user',
        'gender',
        'views',
        'get_percentage_filling',
        'updated',
    )

    list_display_styles = (
        (
            ('updated', ), {
                'align': 'right',
            }
        ),
        (
            ('user', ), {
                'align': 'left',
            }
        ),
        (
            ('get_percentage_filling', 'views', 'gender'), {
                'align': 'center',
            }
        ),
    )

    colored_rows_by = 'determinate_color_rows'

    readonly_fields = (
        'get_user__display_avatar',
        'get_user__get_full_name',
        'display_location',
        'longitude',
        'views',
        'updated',
        'latitude',
    )
    search_fields = ('user', )
    date_hierarchy = 'updated'
    list_filter = (
        'gender',
        'updated',
    )

    form = ProfileAdminModelForm

    def get_fieldsets(self, request, obj=None):

        fieldsets = (
            (
                _('Public information'), {
                    'fields': (
                        'get_user__display_avatar',
                        'about',
                        'crafts',
                        'views',
                        'signature',
                        'on_gmail',
                        'on_github',
                        'on_stackoverflow',
                        'website',
                    ),
                }
            ),
            (
                _('Private information'), {
                    'fields': (
                        'display_location',
                        'gender',
                        'job',
                        'date_birthday',
                        'real_name',
                        'phone',
                        'updated',
                    ),
                }
            ),
            (
                _('Preferences'), {
                    'fields': (
                        'show_email',
                        'show_location',
                    ),
                }
            ),
        )

        return fieldsets

    def determinate_color_rows(self, obj):
        percentage_filling = obj.get_percentage_filling()
        percentage_filling = percentage_filling.strip('%')
        percentage_filling = float(percentage_filling)

        row_color = None
        if percentage_filling >= 90:
            row_color = 'success'
        elif percentage_filling <= 25:
            row_color = 'danger'

        return row_color

    def get_user__display_avatar(self, obj):
        return obj.user.display_avatar()
    get_user__display_avatar.short_description = _('Avatar')

    def get_user__get_full_name(self, obj):
        return obj.user.get_full_name()
    get_user__get_full_name.short_description = _('User')


class UserInline(TabularInline):

    model = User
    fields = ('get_full_name', 'reputation', 'date_joined')
    readonly_fields = ('get_full_name', 'reputation', 'date_joined')
    readonly_fields_tabular_align = {
        'get_full_name': 'left',
        'reputation': 'center',
        'date_joined': 'right',
    }
    max_num = 0
    extra = 0
    can_delete = False


class LevelAdmin(ModelAdmin):
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
    list_display_styles = (
        (
            ('__str__', ), {
                'align': 'left',
            }
        ),
        (
            ('get_count_users', ), {
                'align': 'center',
            }
        ),
        (
            ('name', ), {
                'align': 'center',
            },
        ),
    )
    search_fields = ('name', 'description')
    fieldsets = (
        (
            Level._meta.verbose_name, {
                'fields': (
                    'name',
                    'color',
                    'description',
                ),
            },
        ),
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        qs = qs.levels_with_count_users()
        return qs

    def formfield_for_choice_field(self, db_field, request, **kwargs):

        if db_field.name == "name":
            qs = self.get_queryset(request)
            pk = request.resolver_match.kwargs.get('pk')
            if pk is not None:
                qs = qs.exclude(pk=pk)
            used_level_names = qs.values_list('name', flat=True)
            unused_level_names = [
                choice for choice in db_field.model.CHOICES_LEVEL
                if choice[0] not in used_level_names
            ]

            unused_level_names.insert(0, BLANK_CHOICE_DASH[0])

            kwargs['choices'] = unused_level_names

        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_inline_instances(self, request, obj=None):

        if obj is None:
            return []

        inlines = [UserInline]
        return [inline(self.model, self.site_admin) for inline in inlines]

    def display_color(self, obj):
        """ """

        return format_html(
            '<span style="background-color: {};">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;{}',
            obj.color, obj.color,
        )
    display_color.short_description = Level._meta.get_field('color').verbose_name
    display_color.admin_order_field = 'color'


DefaultSiteAdmin.register_app(UserAppAdmin)

DefaultSiteAdmin.register_model(User, UserAdmin)
DefaultSiteAdmin.register_model(Profile, ProfileAdmin)
DefaultSiteAdmin.register_model(Level, LevelAdmin)
