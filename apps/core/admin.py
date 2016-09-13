
import io
from unittest import mock

from django.http import HttpResponse
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.apps import apps
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings
from django.apps import AppConfig

from utils.django.utils import get_filename_with_datetime


class AppAdmin:
    """

    class BarModelAdmin(admin.ModelAdmin):
       description = 'A bar is a bar is a bar'
       ...

    class FooAppAdmin(admin.AppAdmin):
        app = settings.INSTALLED_APPS[0]
        name = "Foo" # overrides app().name
        description = "An application that does foo"
        style = {'classes' : ('collapse',)}
        order = 1
        models = ( # model order in this list determines their display order in app block
          (BarModel, BarModelAdmin),
          (BazModel, None), # use default ModelAdmin, don't show description
       )

   """

    def get_context_for_tables_of_statistics(self):

        raise NotImplementedError

    def get_context_for_charts_of_statistics(self):

        raise NotImplementedError


class AdminSite(admin.AdminSite):
    """ """

    site_title = _('ProgrammerHelper administration')
    site_header = site_title
    index_title = _('AdminIndex')
    empty_value_display = '-'

    def __init__(self, *args, **kwargs):
        super(AdminSite, self).__init__(*args, **kwargs)
        self._regiter_app_admin = dict()

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

    def get_urls(self):

        urls = super().get_urls()

        # generate string with all custom app`s label for regex, as example: 'tags|books|polls' and etc
        apps_choice = '|'.join(AppConfig.create(conf).label for conf in settings.CUSTOM_APPS)

        urls += [

            # each cuctom app must be have admin page statistics
            url(
                r'^(?P<app_label>{0})/statistics/$'.format(apps_choice),
                self.admin_view(self.statistics_view), {}, 'app_statistics'
            ),

            # each cuctom app must be have admin page for generation reports
            url(
                r'^(?P<app_label>{0})/reports/$'.format(apps_choice),
                self.admin_view(self.reports_view), {}, 'app_reports'
            ),
        ]

        return urls

    @property
    def media(self):
        return admin.ModelAdmin(mock.Mock(), self).media

    def register_app_admin_class(self, appadmin_class):
        """ """

        app_label = appadmin_class.label

        appadmin_class = appadmin_class()

        self._regiter_app_admin[app_label] = appadmin_class

    def statistics_view(self, request, app_label):
        """ """

        template = 'admin/statistics.html'

        app_config = apps.get_app_config(app_label)

        app_name = app_config.verbose_name

        context = dict(
            self.each_context(request),
            title=_('{0} statistics').format(app_name),
            app_name=app_name,
            app_label=app_label,
        )

        # for Django-Suit, especially for left Menu
        request.current_app = self.name

        # get a AppAdmin for the app
        app_admin = self._regiter_app_admin[app_label]

        context['tables_data'] = app_admin.get_context_for_tables_of_statistics()
        context['tables_charts_data'] = app_admin.get_context_for_charts_of_statistics()

        return TemplateResponse(request, template, context)

    def reports_view(self, request, app_label):

        if request.method == 'GET':

            # each custom app must be has template for statistics in own folder templates/app_label/admin/...
            template = '{0}/admin/reports.html'.format(app_label)

            app_config = apps.get_app_config(app_label)

            app_name = app_config.verbose_name

            # for Django-Suit, especially for left Menu
            request.current_app = self.name

            # access to the Django`s built-in the jQuery
            media = admin.ModelAdmin(mock.Mock(), admin.AdminSite()).media

            context = dict(
                self.each_context(request),
                title=_('{0} reports').format(app_name),
                app_name=app_name,
                app_label=app_label,
                media=media,
            )

            # get a AppAdmin for the app
            app_admin = self._regiter_app_admin[app_label]

            app_admin.add_context_to_report_page(context)

            return TemplateResponse(request, template, context)

        elif request.method == 'POST':

            app_config = apps.get_app_config(app_label)
            output_buffer = io.BytesIO()
            type_output_report = request.POST['type_output_report']

            if type_output_report == 'pdf':
                content_type = 'application/pdf'
                extension = 'pdf'
            elif type_output_report == 'excel':
                content_type = 'application/vnd.ms-excel'
                extension = 'xlsx'

            filename = get_filename_with_datetime(app_label.title(), extension)

            response = HttpResponse(content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

            themes = request.POST.getlist('themes')
            themes = ', '.join(themes)

            # get a AppAdmin for the app
            app_admin = self._regiter_app_admin[app_label]

            report = app_admin.get_report(type_output_report, themes)

            output = output_buffer.getvalue()
            output_buffer.close()

            response.write(output)
            return response


AdminSite = AdminSite(name='admin')


def register_models_admin():

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
    from apps.books.admin import BookAdmin, WriterAdmin, PublisherAdmin
    from apps.books.models import Book, Writer, Publisher
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
    from apps.questions.admin import QuestionAdmin, AnswerAdmin, QuestionsAppAdmin
    from apps.questions.models import Question, Answer
    from apps.marks.admin import MarkAdmin
    from apps.marks.models import Mark
    from apps.sessions.admin import ExpandedSessionAdmin
    from apps.sessions.models import ExpandedSession
    from apps.snippets.admin import SnippetAdmin, SnippetAppAdmin
    from apps.snippets.models import Snippet
    from apps.solutions.admin import SolutionAdmin, SolutionAppAdmin
    from apps.solutions.models import Solution
    from apps.tags.admin import TagAdmin
    from apps.tags.models import Tag
    from apps.testing.admin import (
        SuitAdmin, PassageAdmin, QuestionAdmin as TestQuestionAdmin,
        VariantAdmin, TestingAppAdmin
    )
    from apps.testing.models import Suit, Passage, Question as TestQuestion, Variant
    from apps.utilities.admin import UtilitiesAppAdmin, CategoryAdmin as UtilityCategoryAdmin, UtilityAdmin
    from apps.utilities.models import Category as UtilityCategory, Utility

    AdminSite.register_app_admin_class(UtilitiesAppAdmin)
    AdminSite.register_app_admin_class(QuestionsAppAdmin)
    AdminSite.register_app_admin_class(SnippetAppAdmin)
    AdminSite.register_app_admin_class(SolutionAppAdmin)
    AdminSite.register_app_admin_class(TestingAppAdmin)

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
    AdminSite.register(Suit, SuitAdmin)
    AdminSite.register(Passage, PassageAdmin)
    AdminSite.register(TestQuestion, TestQuestionAdmin)
    AdminSite.register(Variant, VariantAdmin)

    # solutions
    AdminSite.register(Solution, SolutionAdmin)

    # questions
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
    AdminSite.register(Writer, WriterAdmin)
    AdminSite.register(Publisher, PublisherAdmin)

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


register_models_admin()
