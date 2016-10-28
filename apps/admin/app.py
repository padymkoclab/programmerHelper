
from django.apps.config import AppConfig
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import url
from django.contrib.auth import get_permission_codename
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.text import capfirst, get_text_list
from django.utils.translation import (
    override as translation_override, string_concat, ugettext as _, ungettext,
)
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView

from .decorators import admin_staff_member_required
from .views import AppIndexView, AppReportView, AppStatisticsView


class AppAdmin:
    """ """

    app_config_class = None

    def __init__(self, site_admin):

        if AppConfig != self.app_config_class.__mro__[1]:
            raise ImproperlyConfigured('Attribute "app_config_class" must be instance of {}'.format(AppConfig))

        self.site_admin = site_admin

        self.app_label = self.get_app_label()

    @classmethod
    def get_app_label(cls):

        if cls.app_config_class is None:
            raise AttributeError('app_config_class must be not None.')

        if AppConfig != cls.app_config_class.__mro__[1]:
            raise ImproperlyConfigured('Attribute "app_config_class" must be instance of {}'.format(AppConfig))

        if hasattr(cls.app_config_class, 'label'):
            return cls.app_config_class.label

        app_labels = [
            app_label for app_label, app_config_class in apps.app_configs.items()
            if isinstance(app_config_class, cls.app_config_class)
        ]

        if len(app_labels) != 1:
            raise ImproperlyConfigured('Do you have app with same name?')

        return app_labels[0]

    @property
    def urls(self):
        return self.get_urls()

    def get_urls(self):

        app_config = apps.get_app_config(self.app_label)

        urlpatterns = [
            url(
                r'^$', kwargs={}, name='{}_index'.format(self.app_label),
                view=admin_staff_member_required(
                    AppIndexView.as_view(site_admin=self.site_admin, app_config=app_config), cacheable=True
                ),
            ),
            url(
                r'^reports/$', kwargs={}, name='{}_reports'.format(self.app_label),
                view=admin_staff_member_required(
                    AppReportView.as_view(site_admin=self.site_admin, app_config=app_config), cacheable=True
                ),
            ),
            url(
                r'^statistics/$', kwargs={}, name='{}_statistics'.format(self.app_label),
                view=admin_staff_member_required(
                    AppStatisticsView.as_view(site_admin=self.site_admin, app_config=app_config)
                ),
            ),
        ]

        return urlpatterns

    def get_tables_of_statistics(self):
        """
        return (
            (_('Books'), (
                (_('Count books'), Book.objects.count()),
                (_('Count russian books'), Book.objects.get_count_russian_books()),
                (_('Count english books'), Book.objects.get_count_english_books()),
                (_('Count great books'), Book.objects.get_count_great_books()),
                (_('Count big books'), Book.objects.get_count_big_books()),
                (_('Count middle books'), Book.objects.get_count_middle_books()),
                (_('Count tiny books'), Book.objects.get_count_tiny_books()),
            )),
        )
        """

        raise NotImplementedError

    def get_context_for_charts_of_statistics(self):
        """
        return (
            {
                'title': _('Chart count books by size'),
                'table': None,
                'chart': Book.objects.get_chart_statistics_count_books_by_size(),
            },
            {
                'title': _('Chart count replies for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count replies')),
                    'data': Book.replies_manager.get_statistics_count_replies_for_the_past_year(),
                },
                'chart': Book.replies_manager.get_chart_count_replies_for_the_past_year(),
            },
        )
        """

        raise NotImplementedError
