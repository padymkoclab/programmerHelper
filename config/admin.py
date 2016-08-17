
from django.template.response import TemplateResponse
from django.apps import apps
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# auth
from apps.users.admin import UserAdmin, UserLevelAdmin
from apps.users.models import User, UserLevel
from django.contrib.auth.models import Group

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

# Temprorary is disabled
#
# from apps.courses.admin import CourseAdmin, LessonAdmin, SublessonAdmin
# from apps.courses.models import Course, Lesson, Sublesson
#
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


class AdminSite(admin.AdminSite):
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


AdminSite = AdminSite(name='admin')


# Register models
#
# users
AdminSite.register(Group)

# users
AdminSite.register(User, UserAdmin)
AdminSite.register(UserLevel, UserLevelAdmin)

# badges
AdminSite.register(Badge, BadgeAdmin)
AdminSite.register(GettingBadge, GettingBadgeAdmin)

# utilities
AdminSite.register(UtilityCategory, UtilityCategoryAdmin)
AdminSite.register(Utility, UtilityAdmin)

# tester
AdminSite.register(TestingSuit, TestingSuitAdmin)
AdminSite.register(TestingPassage, TestingPassageAdmin)
AdminSite.register(TestingQuestion, TestingQuestionAdmin)
AdminSite.register(TestingVariant, TestingVariantAdmin)

# solution
AdminSite.register(SolutionCategory, SolutionCategoryAdmin)
AdminSite.register(Solution, SolutionAdmin)

# question
AdminSite.register(Question, QuestionAdmin)
AdminSite.register(Answer, AnswerAdmin)

# articles
AdminSite.register(Article, ArticleAdmin)
AdminSite.register(ArticleSubsection, ArticleSubsectionAdmin)

# tags
AdminSite.register(Tag, TagAdmin)

# forum
AdminSite.register(ForumSection, ForumSectionAdmin)
AdminSite.register(ForumTopic, ForumTopicAdmin)
AdminSite.register(ForumPost, ForumPostAdmin)

# snippets
AdminSite.register(Snippet, SnippetAdmin)

# newsletters
AdminSite.register(Newsletter, NewsletterAdmin)

# books
AdminSite.register(Book, BookAdmin)
AdminSite.register(Writter, WritterAdmin)

# cources
# AdminSite.register(Course, CourseAdmin)
# AdminSite.register(Lesson, LessonAdmin)
# AdminSite.register(Sublesson, SublessonAdmin)

# polls
AdminSite.register(Poll, PollAdmin)
AdminSite.register(Choice, ChoiceAdmin)
AdminSite.register(Vote, VoteAdmin)

# Apps with generic models
AdminSite.register(Comment, CommentAdmin)
AdminSite.register(Opinion, OpinionAdmin)
AdminSite.register(Mark, MarkAdmin)

# activity
AdminSite.register(Activity, ActivityAdmin)

# notifications
AdminSite.register(Notification, NotificationAdmin)

# sessions
AdminSite.register(ExpandedSession, ExpandedSessionAdmin)
