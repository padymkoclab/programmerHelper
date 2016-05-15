
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from mylabour.admin_listfilters import ListFilterLastLogin
from mylabour.admin_actions import (
    make_accounts_as_non_superuser,
    make_accounts_as_superuser,
    make_accounts_as_non_active,
    make_accounts_as_active,
    )

from .forms import UserChangeForm, UserCreationForm
from .models import AccountLevel


class AccountAdmin(BaseUserAdmin):
    """
    Admin configuration for model Account
    """

    form = UserChangeForm
    add_form = UserCreationForm
    actions = [make_accounts_as_non_superuser, make_accounts_as_superuser, make_accounts_as_non_active, make_accounts_as_active]

    list_display = [
        'email',
        'username',
        'level',
        'is_active',
        'is_superuser',
        'get_count_comments',
        'get_count_opinions',
        'get_count_likes',
        'get_count_scopes',
        # 'get_count_questions',
        # 'get_count_snippets',
        # 'get_count_answers',
        # 'get_count_articles',
        # 'get_count_solutions',
        # 'get_count_posts',
        # 'get_count_topics',
        # 'get_count_test_suits',
        # 'get_count_passages',
        'last_login',
        'date_joined',
    ]
    search_fields = ['email', 'username']
    list_filter = [
        ('level', admin.RelatedOnlyFieldListFilter),
        'is_superuser',
        ListFilterLastLogin,
        'date_joined',
    ]
    date_hierarchy = 'date_joined'
    ordering = ['date_joined']
    #
    radio_fields = {'gender': admin.VERTICAL}
    filter_horizontal = ['groups']
    filter_vertical = ['user_permissions']
    readonly_fields = ['last_login', 'level']
    fieldsets = [
        (
            _('Account detail'), {
                'classes': ['wide'],
                'fields':
                    [
                        'email',
                        'username',
                        'password',
                        'level',
                        'picture',
                    ]
            },
        ),
        (
            _('Personal information'), {
                'fields':
                    [
                        'gender',
                        'real_name',
                        'date_birthday',
                    ]
            }
        ),
        (
            _('Presents in web'), {
                'fields':
                    [
                        'presents_on_gmail',
                        'presents_on_github',
                        'presents_on_stackoverflow',
                        'personal_website',
                    ]
            }
        ),
        (
            _('Permissions'), {
                'fields': [
                    'is_active',
                    'is_superuser',
                    'user_permissions',
                    'groups',
                ]
            }
        ),
    ]
    add_fieldsets = [
        (
            None, {
                'fields': [
                    'email',
                    'username',
                    'password1',
                    'password2',
                    'date_birthday',
                ]
            }
        )
    ]

    def get_queryset(self, request):
        qs = super(AccountAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_comments=models.Count('comments', distinct=True),
            count_opinions=models.Count('opinions', distinct=True),
            count_likes=models.Count('likes', distinct=True),
            count_scopes=models.Count('scopes', distinct=True),
            # count_articles=models.Count('articles', distinct=True),
            # count_answers=models.Count('answers', distinct=True),
            # count_posts=models.Count('posts', distinct=True),
            # count_solutions=models.Count('solutions', distinct=True),
            # count_topics=models.Count('topics', distinct=True),
            # count_questions=models.Count('questions', distinct=True),
            # count_snippets=models.Count('snippets', distinct=True),
            # count_courses=models.Count('courses', distinct=True),
            # count_test_suits=models.Count('test_suits', distinct=True),
            # count_passages=models.Count('passages', distinct=True),
        )
        return qs

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_likes(self, obj):
        return obj.count_likes
    get_count_likes.admin_order_field = 'count_likes'
    get_count_likes.short_description = _('Count likes')

    def get_count_scopes(self, obj):
        return obj.count_scopes
    get_count_scopes.admin_order_field = 'count_scopes'
    get_count_scopes.short_description = _('Count scopes')

    def get_count_questions(self, obj):
        return obj.count_questions
    get_count_questions.admin_order_field = 'count_questions'
    get_count_questions.short_description = _('Count questions')

    def get_count_snippets(self, obj):
        return obj.count_snippets
    get_count_snippets.admin_order_field = 'count_snippets'
    get_count_snippets.short_description = _('Count snippets')

    def get_count_articles(self, obj):
        return obj.count_articles
    get_count_articles.admin_order_field = 'count_articles'
    get_count_articles.short_description = _('Count article')

    def get_count_answers(self, obj):
        return obj.count_answers
    get_count_answers.admin_order_field = 'count_answers'
    get_count_answers.short_description = _('Count answers')

    def get_count_solutions(self, obj):
        return obj.count_solutions
    get_count_solutions.admin_order_field = 'count_solutions'
    get_count_solutions.short_description = _('Count solutions')

    def get_count_posts(self, obj):
        return obj.count_posts
    get_count_posts.admin_order_field = 'count_posts'
    get_count_posts.short_description = _('Count posts')

    def get_count_topics(self, obj):
        return obj.count_topics
    get_count_topics.admin_order_field = 'count_topics'
    get_count_topics.short_description = _('Count topics')

    def get_count_test_suits(self, obj):
        return obj.count_test_suits
    get_count_test_suits.admin_order_field = 'count_test_suits'
    get_count_test_suits.short_description = _('Count test suits')

    def get_count_passages(self, obj):
        return obj.count_passages
    get_count_passages.admin_order_field = 'count_passages'
    get_count_passages.short_description = _('Count passages')


class AccountLevelAdmin(admin.ModelAdmin):
    '''
    Admin View for AccountLevel
    '''

    list_display = ('name', 'get_count_accounts', 'color', 'description')
    search_fields = ('name',)
    fieldsets = [
        [
            AccountLevel._meta.verbose_name, {
                'fields': ['name', 'color', 'description']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(AccountLevelAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_accounts=models.Count('accounts'),
        )
        return qs

    def get_count_accounts(self, obj):
        return obj.count_accounts
    get_count_accounts.admin_order_field = 'count_accounts'
    get_count_accounts.short_description = _('Count accounts')
