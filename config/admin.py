
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# auth
from apps.accounts.admin import AccountAdmin, AccountLevelAdmin
from apps.accounts.models import Account, AccountLevel
from django.contrib.auth.models import Group
# from django.contrib.sessions.models import Session

from mylabour.admin_actions import export_as_csv, export_as_json, export_as_xml, export_as_yaml, export_as_xlsx

# apps
from apps.actions.admin import ActionAdmin
from apps.actions.models import Action
from apps.articles.admin import ArticleAdmin, ArticleSubsectionAdmin
from apps.articles.models import Article, ArticleSubsection
from apps.badges.admin import BadgeAdmin, GettingBadgeAdmin
from apps.badges.models import Badge, GettingBadge
from apps.books.admin import BookAdmin, WritterAdmin
from apps.books.models import Book, Writter
from apps.comments.admin import CommentAdmin
from apps.comments.models import Comment
from apps.courses.admin import CourseAdmin, LessonAdmin, SublessonAdmin
from apps.courses.models import Course, Lesson, Sublesson
from apps.forum.admin import ForumSectionAdmin, ForumTopicAdmin, ForumPostAdmin
from apps.forum.models import ForumSection, ForumTopic, ForumPost
from apps.inboxes.admin import InboxAdmin
from apps.inboxes.models import Inbox
from apps.newsletters.admin import NewsletterAdmin
from apps.newsletters.models import Newsletter
from apps.opinions.admin import OpinionAdmin
from apps.opinions.models import Opinion
from apps.polls.admin import PollAdmin, VoteInPollAdmin, ChoiceAdmin
from apps.polls.models import Poll, Choice, VoteInPoll
from apps.questions.admin import QuestionAdmin, AnswerAdmin
from apps.questions.models import Question, Answer
from apps.scopes.admin import ScopeAdmin
from apps.scopes.models import Scope
from apps.sessions.admin import ExpandedSessionAdmin
from apps.sessions.models import ExpandedSession
from apps.snippets.admin import SnippetAdmin
from apps.snippets.models import Snippet
from apps.solutions.admin import SolutionCategoryAdmin, SolutionAdmin
from apps.solutions.models import SolutionCategory, Solution
from apps.tags.admin import TagAdmin
from apps.tags.models import Tag
from apps.testing.admin import TestingSuitAdmin, TestingPassageAdmin, TestingQuestionAdmin, TestingVariantAdmin
from apps.testing.models import TestingSuit, TestingPassage, TestingQuestion, TestingVariant
from apps.utilities.admin import UtilityCategoryAdmin, UtilityAdmin
from apps.utilities.models import UtilityCategory, Utility
from apps.web_links.admin import WebLinkAdmin
from apps.web_links.models import WebLink


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
# accounts
ProgrammerHelper_AdminSite.register(Account, AccountAdmin)
ProgrammerHelper_AdminSite.register(AccountLevel, AccountLevelAdmin)
# badges
ProgrammerHelper_AdminSite.register(Badge, BadgeAdmin)
ProgrammerHelper_AdminSite.register(GettingBadge, GettingBadgeAdmin)
# programming_utilities
ProgrammerHelper_AdminSite.register(UtilityCategory, UtilityCategoryAdmin)
ProgrammerHelper_AdminSite.register(Utility, UtilityAdmin)
# web_links
ProgrammerHelper_AdminSite.register(WebLink, WebLinkAdmin)
# programming_tester
ProgrammerHelper_AdminSite.register(TestingSuit, TestingSuitAdmin)
ProgrammerHelper_AdminSite.register(TestingPassage, TestingPassageAdmin)
ProgrammerHelper_AdminSite.register(TestingQuestion, TestingQuestionAdmin)
ProgrammerHelper_AdminSite.register(TestingVariant, TestingVariantAdmin)
# solution
ProgrammerHelper_AdminSite.register(SolutionCategory, SolutionCategoryAdmin)
ProgrammerHelper_AdminSite.register(Solution, SolutionAdmin)
# question
ProgrammerHelper_AdminSite.register(Question, QuestionAdmin)
ProgrammerHelper_AdminSite.register(Answer, AnswerAdmin)
# articles
ProgrammerHelper_AdminSite.register(Article, ArticleAdmin)
ProgrammerHelper_AdminSite.register(ArticleSubsection, ArticleSubsectionAdmin)
# tags
ProgrammerHelper_AdminSite.register(Tag, TagAdmin)
# forum
ProgrammerHelper_AdminSite.register(ForumSection, ForumSectionAdmin)
ProgrammerHelper_AdminSite.register(ForumTopic, ForumTopicAdmin)
ProgrammerHelper_AdminSite.register(ForumPost, ForumPostAdmin)
# snippets
ProgrammerHelper_AdminSite.register(Snippet, SnippetAdmin)
# newsletters
ProgrammerHelper_AdminSite.register(Newsletter, NewsletterAdmin)
# books
ProgrammerHelper_AdminSite.register(Book, BookAdmin)
ProgrammerHelper_AdminSite.register(Writter, WritterAdmin)
# cources
ProgrammerHelper_AdminSite.register(Course, CourseAdmin)
ProgrammerHelper_AdminSite.register(Lesson, LessonAdmin)
ProgrammerHelper_AdminSite.register(Sublesson, SublessonAdmin)
# polls
ProgrammerHelper_AdminSite.register(Poll, PollAdmin)
ProgrammerHelper_AdminSite.register(Choice, ChoiceAdmin)
ProgrammerHelper_AdminSite.register(VoteInPoll, VoteInPollAdmin)
# Apps with generic models
ProgrammerHelper_AdminSite.register(Comment, CommentAdmin)
ProgrammerHelper_AdminSite.register(Opinion, OpinionAdmin)
ProgrammerHelper_AdminSite.register(Scope, ScopeAdmin)
# actions
ProgrammerHelper_AdminSite.register(Action, ActionAdmin)
# inboxes
ProgrammerHelper_AdminSite.register(Inbox, InboxAdmin)
# sessions
ProgrammerHelper_AdminSite.register(ExpandedSession, ExpandedSessionAdmin)
