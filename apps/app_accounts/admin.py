
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.app_solutions.models import (
    Answer, SolutionComment, Question, AnswerComment, OpinionAboutAnswer, OpinionAboutSolution, OpinionAboutQuestion
    )
from apps.app_snippets.models import Snippet, SnippetComment, OpinionAboutSnippet
from apps.app_articles.models import Article, ArticleComment, OpinionAboutArticle
from apps.app_badges.models import Badge
from apps.app_newsletters.models import Newsletter
from apps.app_programming_tester.models import TestSuit
from apps.app_forum.models import ForumTopic, ForumPost
from mylabour.admin_listfilters import ListFilterLastLogin
from mylabour.admin_actions import (
    make_accounts_as_non_superuser,
    make_accounts_as_superuser,
    make_accounts_as_non_active,
    make_accounts_as_active,
    )

from .forms import UserChangeForm, UserCreationForm


class OpinionAboutAnswerInline(admin.StackedInline):
    '''
    Stacked Inline View for OpinionAboutAnswer
    '''

    model = OpinionAboutAnswer
    extra = 1
    verbose_name = _('Opinion')


class OpinionAboutSolutionInline(admin.StackedInline):
    '''
    Stacked Inline View for OpinionAboutSolution
    '''

    model = OpinionAboutSolution
    extra = 1
    verbose_name = _('Opinion')


class OpinionAboutQuestion(admin.StackedInline):
    '''
    Stacked Inline View for OpinionAboutQuestion
    '''

    model = OpinionAboutQuestion
    extra = 1
    verbose_name = _('Opinion')


class OpinionAboutArticleInline(admin.StackedInline):
    '''
    Stacked Inline View for OpinionAboutArticle
    '''

    model = OpinionAboutArticle
    extra = 1
    verbose_name = _('Opinion')


class OpinionAboutSnippetInline(admin.StackedInline):
    '''
    Stacked Inline View for OpinionAboutSnippet
    '''

    model = OpinionAboutSnippet
    extra = 1
    fieldsets = [
        [None, {
            'fields': ['snippet', 'is_useful', 'is_favorite']
        }]
    ]
    verbose_name = _('Opinion')


class NewsletterInline(admin.StackedInline):
    '''
    Stacked Inline View for Newsletter
    '''

    model = Newsletter
    extra = 1


class TestSuitInline(admin.StackedInline):
    '''
    Stacked Inline View for TestSuit
    '''

    model = TestSuit
    extra = 1
    verbose_name = _('Suit')


class TopicInline(admin.StackedInline):
    '''
    Stacked Inline View for ForumTopic
    '''

    model = ForumTopic
    extra = 1


class ForumPostInline(admin.StackedInline):
    '''
    Stacked Inline View for ForumPost
    '''

    model = ForumPost
    extra = 1


class AnswerInline(admin.StackedInline):
    '''
    Stacked Inline View for Answer
    '''

    model = Answer
    extra = 1
    verbose_name = _('Answer')


class ArticleInline(admin.StackedInline):
    '''
    Stacked Inline View for Article
    '''

    model = Article
    extra = 1
    verbose_name = _('Article')


class SolutionCommentInline(admin.StackedInline):
    '''
    Stacked Inline View for SolutionComment
    '''

    model = SolutionComment
    extra = 1
    verbose_name = _('Comment')


class BadgeInline(admin.StackedInline):
    '''
    Stacked Inline View for Badge
    '''

    model = Badge
    extra = 1


class QuestionInline(admin.StackedInline):
    '''
    Stacked Inline View for Question
    '''

    model = Question
    extra = 1
    verbose_name = _('Question')


class AnswerCommentInline(admin.StackedInline):
    '''
    Stacked Inline View for AnswerComment
    '''

    model = AnswerComment
    extra = 1
    verbose_name = _('Comment')


class SnippetInline(admin.StackedInline):
    '''
    Stacked Inline View for Snippet
    '''

    model = Snippet
    extra = 1
    verbose_name = _('Snippet')


class SnippetCommentInline(admin.StackedInline):
    '''
    Stacked Inline View for SnippetComment
    '''

    model = SnippetComment
    extra = 1
    verbose_name = _('Comment')


class ArticleCommentInline(admin.StackedInline):
    '''
    Stacked Inline View for ArticleComment
    '''

    model = ArticleComment
    extra = 1
    verbose_name = _('Comment')


class AccountAdmin(BaseUserAdmin):
    """
    Admin configuration for model Account
    """

    form = UserChangeForm
    add_form = UserCreationForm
    actions = [make_accounts_as_non_superuser, make_accounts_as_superuser, make_accounts_as_non_active, make_accounts_as_active]

    list_display = ['email', 'username', 'account_type', 'is_active', 'is_superuser', 'last_login', 'date_joined']
    search_fields = ['email', 'username']
    list_filter = ['account_type', 'is_superuser', ListFilterLastLogin, 'date_joined']
    date_hierarchy = 'date_joined'
    ordering = ['date_joined']
    #
    radio_fields = {'gender': admin.VERTICAL}
    filter_horizontal = ['groups']
    filter_vertical = ['user_permissions']
    readonly_fields = ['last_login']
    fieldsets = [
        (
            _('Account information'), {
                'classes': ['wide'],
                'fields':
                    [
                        'email',
                        'username',
                        'password',
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
    inlines = [
        # ArticleInline,
        # ArticleCommentInline,
        # SolutionCommentInline,
        # QuestionInline,
        # AnswerInline,
        # AnswerCommentInline,
        # SnippetInline,
        # SnippetCommentInline,
        # NewsletterInline,
        # TestSuitInline,
        # TopicInline,
        # ForumPostInline,
        # OpinionAboutSnippetInline,
        # OpinionAboutAnswerInline,
        # OpinionAboutSolutionInline,
        # OpinionAboutArticleInline,
    ]


class AccountAdminArticles(admin.ModelAdmin):
    '''
    Admin View for Account
    '''

    pass
    # list_display = ('email',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
