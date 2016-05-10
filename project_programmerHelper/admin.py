
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# auth
from apps.app_accounts.models import Account
from apps.app_accounts.admin import AccountAdmin
from django.contrib.auth.models import Group
#
from apps.app_articles.admin import ArticleAdmin, ArticleSubsectionAdmin
from apps.app_articles.models import Article, ArticleSubsection
from apps.app_badges.admin import BadgeAdmin, GettingBadgeAdmin
from apps.app_badges.models import Badge, GettingBadge
from apps.app_books.admin import BookAdmin, WritterAdmin
from apps.app_books.models import Book, Writter
from apps.app_courses.admin import CourseAdmin, LessonAdmin, SublessonAdmin
from apps.app_courses.models import Course, Lesson, Sublesson
from apps.app_forum.admin import ForumThemeAdmin, ForumTopicAdmin, ForumPostAdmin
from apps.app_forum.models import ForumTopic, ForumTheme, ForumPost
from apps.app_generic_models.admin import CommentGenericAdmin, OpinionGenericAdmin, LikeGenericAdmin, ScopeGenericAdmin
from apps.app_generic_models.models import CommentGeneric, OpinionGeneric, LikeGeneric, ScopeGeneric
from apps.app_newsletters.admin import NewsletterAdmin
from apps.app_newsletters.models import Newsletter
from apps.app_polls.admin import PollAdmin, VoteInPollAdmin, ChoiceAdmin
from apps.app_polls.models import Poll, Choice, VoteInPoll
from apps.app_testing.admin import TestingSuitAdmin, TestingQuestionAdmin, TestingVariantAdmin
from apps.app_testing.models import TestingSuit, TestingQuestion, TestingVariant
from apps.app_utilities.admin import UtilityCategoryAdmin, UtilityAdmin
from apps.app_utilities.models import UtilityCategory, Utility
from apps.app_questions.admin import QuestionAdmin, AnswerAdmin
from apps.app_questions.models import Question, Answer
from apps.app_snippets.admin import SnippetAdmin
from apps.app_snippets.models import Snippet
from apps.app_solutions.admin import SolutionCategoryAdmin, SolutionAdmin
from apps.app_solutions.models import SolutionCategory, Solution
from apps.app_tags.admin import TagAdmin
from apps.app_tags.models import Tag
from apps.app_web_links.admin import WebLinkAdmin
from apps.app_web_links.models import WebLink


class MyAdminSite(admin.AdminSite):
    site_header = _('Admin part of website')
    site_title = _('Monty Python administration')
    index_title = _('Website ProgrammerHelper')
    empty_value_display = '-'


ProgrammerHelper_AdminSite = MyAdminSite(name='ProgrammerHelper')
ProgrammerHelper_AdminSite.register(Group)
# app_accounts
ProgrammerHelper_AdminSite.register(Account, AccountAdmin)
# ProgrammerHelper_AdminSite.register(Account, AccountAdminArticles)
# app_badges
ProgrammerHelper_AdminSite.register(Badge, BadgeAdmin)
ProgrammerHelper_AdminSite.register(GettingBadge, GettingBadgeAdmin)
# app_programming_utilities
ProgrammerHelper_AdminSite.register(UtilityCategory, UtilityCategoryAdmin)
ProgrammerHelper_AdminSite.register(Utility, UtilityAdmin)
# app_web_links
ProgrammerHelper_AdminSite.register(WebLink, WebLinkAdmin)
# app_programming_tester
ProgrammerHelper_AdminSite.register(TestingSuit, TestingSuitAdmin)
ProgrammerHelper_AdminSite.register(TestingQuestion, TestingQuestionAdmin)
ProgrammerHelper_AdminSite.register(TestingVariant, TestingVariantAdmin)
# app_solution
ProgrammerHelper_AdminSite.register(SolutionCategory, SolutionCategoryAdmin)
ProgrammerHelper_AdminSite.register(Solution, SolutionAdmin)
# app_question
ProgrammerHelper_AdminSite.register(Question, QuestionAdmin)
ProgrammerHelper_AdminSite.register(Answer, AnswerAdmin)
# app_articles
ProgrammerHelper_AdminSite.register(Article, ArticleAdmin)
ProgrammerHelper_AdminSite.register(ArticleSubsection, ArticleSubsectionAdmin)
# app_tags
ProgrammerHelper_AdminSite.register(Tag, TagAdmin)
# app_forum
ProgrammerHelper_AdminSite.register(ForumTheme, ForumThemeAdmin)
ProgrammerHelper_AdminSite.register(ForumTopic, ForumTopicAdmin)
ProgrammerHelper_AdminSite.register(ForumPost, ForumPostAdmin)
# app_snippets
ProgrammerHelper_AdminSite.register(Snippet, SnippetAdmin)
# app_newsletters
ProgrammerHelper_AdminSite.register(Newsletter, NewsletterAdmin)
# app_books
ProgrammerHelper_AdminSite.register(Book, BookAdmin)
ProgrammerHelper_AdminSite.register(Writter, WritterAdmin)
# app_cources
ProgrammerHelper_AdminSite.register(Course, CourseAdmin)
ProgrammerHelper_AdminSite.register(Lesson, LessonAdmin)
ProgrammerHelper_AdminSite.register(Sublesson, SublessonAdmin)
# app_polls
ProgrammerHelper_AdminSite.register(Poll, PollAdmin)
ProgrammerHelper_AdminSite.register(Choice, ChoiceAdmin)
ProgrammerHelper_AdminSite.register(VoteInPoll, VoteInPollAdmin)
# app_generic_models
ProgrammerHelper_AdminSite.register(CommentGeneric, CommentGenericAdmin)
ProgrammerHelper_AdminSite.register(OpinionGeneric, OpinionGenericAdmin)
ProgrammerHelper_AdminSite.register(LikeGeneric, LikeGenericAdmin)
ProgrammerHelper_AdminSite.register(ScopeGeneric, ScopeGenericAdmin)
