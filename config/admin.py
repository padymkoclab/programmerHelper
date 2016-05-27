
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# auth
from apps.app_accounts.admin import AccountAdmin, AccountLevelAdmin
from apps.app_accounts.models import Account, AccountLevel
from django.contrib.auth.models import Group
# from django.contrib.sessions.models import Session

from mylabour.admin_actions import export_as_csv, export_as_json, export_as_xml, export_as_yaml, export_as_xlsx

# apps
from apps.app_articles.admin import ArticleAdmin, ArticleSubsectionAdmin
from apps.app_articles.models import Article, ArticleSubsection
from apps.app_badges.admin import BadgeAdmin, GettingBadgeAdmin
from apps.app_badges.models import Badge, GettingBadge
from apps.app_books.admin import BookAdmin, WritterAdmin
from apps.app_books.models import Book, Writter
from apps.app_courses.admin import CourseAdmin, LessonAdmin, SublessonAdmin
from apps.app_courses.models import Course, Lesson, Sublesson
from apps.app_forum.admin import ForumSectionAdmin, ForumTopicAdmin, ForumPostAdmin
from apps.app_forum.models import ForumSection, ForumTopic, ForumPost
from apps.app_generic_models.admin import CommentGenericAdmin, OpinionGenericAdmin, LikeGenericAdmin, ScopeGenericAdmin
from apps.app_generic_models.models import CommentGeneric, OpinionGeneric, LikeGeneric, ScopeGeneric
from apps.app_newsletters.admin import NewsletterAdmin
from apps.app_newsletters.models import Newsletter
from apps.app_polls.admin import PollAdmin, VoteInPollAdmin, ChoiceAdmin
from apps.app_polls.models import Poll, Choice, VoteInPoll
from apps.app_questions.admin import QuestionAdmin, AnswerAdmin
from apps.app_questions.models import Question, Answer
from apps.app_snippets.admin import SnippetAdmin
from apps.app_snippets.models import Snippet
from apps.app_solutions.admin import SolutionCategoryAdmin, SolutionAdmin
from apps.app_solutions.models import SolutionCategory, Solution
from apps.app_tags.admin import TagAdmin
from apps.app_tags.models import Tag
from apps.app_testing.admin import TestingSuitAdmin, TestingPassageAdmin, TestingQuestionAdmin, TestingVariantAdmin
from apps.app_testing.models import TestingSuit, TestingPassage, TestingQuestion, TestingVariant
from apps.app_utilities.admin import UtilityCategoryAdmin, UtilityAdmin
from apps.app_utilities.models import UtilityCategory, Utility
from apps.app_web_links.admin import WebLinkAdmin
from apps.app_web_links.models import WebLink
from apps.app_actions.models import Action
from apps.app_actions.admin import ActionAdmin
from apps.app_inboxes.models import Inbox
from apps.app_inboxes.admin import InboxAdmin
from apps.app_sessions.models import ExpandedSession
from apps.app_sessions.admin import ExpandedSessionAdmin


class ProgrammerHelperSite(admin.AdminSite):
    site_header = _('Admin part of website')
    site_title = _('Monty Python administration')
    index_title = _('Website ProgrammerHelper')
    empty_value_display = '-'


ProgrammerHelper_AdminSite = ProgrammerHelperSite(name='ProgrammerHelper')

ProgrammerHelper_AdminSite.add_action(export_as_csv)
ProgrammerHelper_AdminSite.add_action(export_as_json)
ProgrammerHelper_AdminSite.add_action(export_as_xml)
ProgrammerHelper_AdminSite.add_action(export_as_yaml)
ProgrammerHelper_AdminSite.add_action(export_as_xlsx)

ProgrammerHelper_AdminSite.register(Group)
# app_accounts
ProgrammerHelper_AdminSite.register(Account, AccountAdmin)
ProgrammerHelper_AdminSite.register(AccountLevel, AccountLevelAdmin)
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
ProgrammerHelper_AdminSite.register(TestingPassage, TestingPassageAdmin)
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
ProgrammerHelper_AdminSite.register(ForumSection, ForumSectionAdmin)
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
# app_actions
ProgrammerHelper_AdminSite.register(Action, ActionAdmin)
# app_inboxes
ProgrammerHelper_AdminSite.register(Inbox, InboxAdmin)

ProgrammerHelper_AdminSite.register(ExpandedSession, ExpandedSessionAdmin)
