
from django.template.response import TemplateResponse
from django.apps import apps
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# auth
from apps.users.admin import UserAdmin, UserLevelAdmin
from apps.users.models import User, UserLevel
from django.contrib.auth.models import Group

from mylabour.admin_actions import export_as_csv, export_as_json, export_as_xml, export_as_yaml, export_as_xlsx

# apps
from apps.activity.admin import ActivityAdmin
from apps.activity.models import Activity
from apps.articles.admin import ArticleAdmin, ArticleSubsectionAdmin
from apps.articles.models import Article, ArticleSubsection
from apps.badges.admin import BadgeAdmin, GettingBadgeAdmin
from apps.badges.models import Badge, GettingBadge
from apps.books.admin import BookAdmin, WritterAdmin
from apps.books.models import Book, Writter
from apps.comments.admin import CommentAdmin
from apps.comments.models import Comment
# from apps.courses.admin import CourseAdmin, LessonAdmin, SublessonAdmin
# from apps.courses.models import Course, Lesson, Sublesson
from apps.forum.admin import ForumSectionAdmin, ForumTopicAdmin, ForumPostAdmin
from apps.forum.models import ForumSection, ForumTopic, ForumPost
from apps.notifications.admin import NotificationAdmin
from apps.notifications.models import Notification
from apps.newsletters.admin import NewsletterAdmin
from apps.newsletters.models import Newsletter
from apps.opinions.admin import OpinionAdmin
from apps.opinions.models import Opinion
from apps.polls.admin import PollAdmin, VoteAdmin, ChoiceAdmin
from apps.polls.models import Poll, Choice, Vote
from apps.questions.admin import QuestionAdmin, AnswerAdmin
from apps.questions.models import Question, Answer
from apps.marks.admin import MarkAdmin
from apps.marks.models import Mark
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


class ProgrammerHelperSite(admin.AdminSite):
    site_title = _('ProgrammerHelper administration')
    site_header = site_title
    index_title = _('AdminIndex')
    empty_value_display = '-'

    def app_index(self, request, app_label, extra_context=None):

        # code from Django 1.9.5
        # code here: ~/.virtualenvs/{virtual_env_name}/lib/python3.4/site-packages/django/contrib/admin/sites.py

        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['name'])
        app_name = apps.get_app_config(app_label).verbose_name
        context = dict(
            self.each_context(request),
            title=_('%(app)s administration') % {'app': app_name},
            app_list=[app_dict],
            app_label=app_label,
        )
        context.update(extra_context or {})

        request.current_app = self.name

        # OWN CHANGES

        # add a first place for a template`s seach in an each app
        places_for_search = [
            '%s/admin/app_index.html' % app_label,
            'admin/app_index.html'
        ]

        return TemplateResponse(request, self.app_index_template or places_for_search, context)


ProgrammerHelperAdminSite = ProgrammerHelperSite(name='admin')

ProgrammerHelperAdminSite.add_action(export_as_csv)
ProgrammerHelperAdminSite.add_action(export_as_json)
ProgrammerHelperAdminSite.add_action(export_as_xml)
ProgrammerHelperAdminSite.add_action(export_as_yaml)
ProgrammerHelperAdminSite.add_action(export_as_xlsx)

ProgrammerHelperAdminSite.register(Group)

# users
ProgrammerHelperAdminSite.register(User, UserAdmin)
ProgrammerHelperAdminSite.register(UserLevel, UserLevelAdmin)

# badges
ProgrammerHelperAdminSite.register(Badge, BadgeAdmin)
ProgrammerHelperAdminSite.register(GettingBadge, GettingBadgeAdmin)

# utilities
ProgrammerHelperAdminSite.register(UtilityCategory, UtilityCategoryAdmin)
ProgrammerHelperAdminSite.register(Utility, UtilityAdmin)

# tester
ProgrammerHelperAdminSite.register(TestingSuit, TestingSuitAdmin)
ProgrammerHelperAdminSite.register(TestingPassage, TestingPassageAdmin)
ProgrammerHelperAdminSite.register(TestingQuestion, TestingQuestionAdmin)
ProgrammerHelperAdminSite.register(TestingVariant, TestingVariantAdmin)

# solution
ProgrammerHelperAdminSite.register(SolutionCategory, SolutionCategoryAdmin)
ProgrammerHelperAdminSite.register(Solution, SolutionAdmin)

# question
ProgrammerHelperAdminSite.register(Question, QuestionAdmin)
ProgrammerHelperAdminSite.register(Answer, AnswerAdmin)

# articles
ProgrammerHelperAdminSite.register(Article, ArticleAdmin)
ProgrammerHelperAdminSite.register(ArticleSubsection, ArticleSubsectionAdmin)

# tags
ProgrammerHelperAdminSite.register(Tag, TagAdmin)

# forum
ProgrammerHelperAdminSite.register(ForumSection, ForumSectionAdmin)
ProgrammerHelperAdminSite.register(ForumTopic, ForumTopicAdmin)
ProgrammerHelperAdminSite.register(ForumPost, ForumPostAdmin)

# snippets
ProgrammerHelperAdminSite.register(Snippet, SnippetAdmin)

# newsletters
ProgrammerHelperAdminSite.register(Newsletter, NewsletterAdmin)

# books
ProgrammerHelperAdminSite.register(Book, BookAdmin)
ProgrammerHelperAdminSite.register(Writter, WritterAdmin)

# cources
# ProgrammerHelperAdminSite.register(Course, CourseAdmin)
# ProgrammerHelperAdminSite.register(Lesson, LessonAdmin)
# ProgrammerHelperAdminSite.register(Sublesson, SublessonAdmin)

# polls
ProgrammerHelperAdminSite.register(Poll, PollAdmin)
ProgrammerHelperAdminSite.register(Choice, ChoiceAdmin)
ProgrammerHelperAdminSite.register(Vote, VoteAdmin)

# Apps with generic models
ProgrammerHelperAdminSite.register(Comment, CommentAdmin)
ProgrammerHelperAdminSite.register(Opinion, OpinionAdmin)
ProgrammerHelperAdminSite.register(Mark, MarkAdmin)

# activity
ProgrammerHelperAdminSite.register(Activity, ActivityAdmin)

# notifications
ProgrammerHelperAdminSite.register(Notification, NotificationAdmin)

# sessions
ProgrammerHelperAdminSite.register(ExpandedSession, ExpandedSessionAdmin)
