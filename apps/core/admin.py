
import abc
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


class AppAdmin(abc.ABC):
    """ """

    @abc.abstractmethod
    def get_context_for_tables_of_statistics(self):
        pass

    @abc.abstractmethod
    def get_context_for_charts_of_statistics(self):
        pass


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

        apps_choice = '|'.join(self._regiter_app_admin.keys())

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
        app_admin = self._regiter_app_admin.get(app_label, None)

        if app_admin is not None:
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
