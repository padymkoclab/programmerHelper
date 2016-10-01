
import logging

from django.core.urlresolvers import reverse
from django.conf.urls import url, include
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
# from django.db.models.base import ModelBase
# from django.template.response import TemplateResponse
# from django.urls import NoReverseMatch
# from django.utils import six
# from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_permission_codename
from django.views.decorators.csrf import csrf_protect
# from django.views.i18n import JavaScriptCatalog
# from django.template.defaultfilters import truncatechars
# from django.contrib import admin

from .views import IndexView, LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, AppIndexView, SettingsView, ImportView, ExportView
from .decorators import admin_staff_member_required
from .admin import ModelAdmin
from .exceptions import AlreadyRegisteredModel, AlreadyRegisteredApp
# actions


logging = logging.getLogger('django.development')


system_check_errors = []


class SiteAdmin:

    admin_site_header = _('Admin part')

    show_calendar = True
    type_calendar = 'Form or Other Media object'
    # (Viewing calendar, adding events, dragging events)
    Full_Calendar = True

    WYSIWYG_Editors = ('TinyMCE', 'CREditor', 'Aloha Editor')

    Media_Gallery = True

    # Text to put at the top of the admin index page.
    # index_title = ugettext_lazy('Site administration')

    # URL for the "View site" link at the top of each admin page.
    # site_url = '/'

    _empty_value_display = '-'

    login_form = None
    index_template = None
    app_index_template = None
    login_template = None
    logout_template = None
    password_change_template = None
    password_change_done_template = None

    def __init__(self, name='admin'):
        self._registry_models = {}
        self._registry_apps = {}
        self._registry_other = {}
        self.name = name
        # self._actions = {'delete_selected': actions.delete_selected}
        # self._global_actions = self._actions.copy()

    @property
    def empty_value_display(self):
        return self._empty_value_display

    @empty_value_display.setter
    def empty_value_display(self, empty_value_display):
        self._empty_value_display = empty_value_display

    def has_permission(self, request):
        """
        Returns True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

    def each_context(self, request):

        # script_name = request.META['SCRIPT_NAME']
        # site_url = script_name if self.site_url == '/' and script_name else self.site_url

        return {
            'admin_site_header': self.admin_site_header,
            'index_url': reverse('admin:index'),
            'has_permission': self.has_permission(request),
            'avaliable_apps_with_models': self.get_avaliable_apps_with_models(request),
            # 'urls_to_active_object': self.get_urls_to_active_object(request),
        }

    def get_urls(self):

        # AdminPart site urls
        urlpatterns = [
            url(r'^$', admin_staff_member_required(IndexView.as_view(site_admin=self)), {}, 'index'),
            url(r'^login/$', csrf_protect(never_cache(LoginView.as_view())), {}, 'login'),
            url(r'^logout/$', admin_staff_member_required(LogoutView.as_view()), {}, 'logout'),
            url(r'^password_change/$', admin_staff_member_required(PasswordChangeView.as_view(), cacheable=True), {}, 'password_change'),
            url(r'^password_change/done/$', admin_staff_member_required(PasswordChangeDoneView.as_view(), cacheable=True), {}, 'password_change_done'),
            url(r'^settings/$', SettingsView.as_view(), {}, 'settings'),
            url(r'^import/$', ImportView.as_view(), {}, 'import'),
            url(r'^export/$', ExportView.as_view(), {}, 'export'),
            # url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
        ]

        # App urls
        for app_label, app_admin in self._registry_apps.items():
            urlpatterns += [
                url(r'{}/'.format(app_label), include(app_admin.urls)),
            ]

        # Model urls
        for model, model_admin in self._registry_models.items():

            urlpatterns += [
                url(r'{}/{}/'.format(model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name

    def register_model(self, model, model_admin_class):
        """
        """

        if model._meta.abstract:
            raise ImproperlyConfigured(
                'The model {} is abstract, so it cannot be registered with admin.'.format(model._meta.model_name)
            )

        if model in self._registry_models:
            raise AlreadyRegisteredModel('The model {} is already registered'.format(model._meta.model_name))

        # Ignore the registration if the model has been
        # swapped out.
        if not model._meta.swapped:

            # Instantiate the admin class to save in the registry
            model_admin = model_admin_class(model, self)
            # if model_admin_class is not ModelAdmin and settings.DEBUG:
            #     system_check_errors.extend(model_admin.check())

            self._registry_models[model] = model_admin

    def register_app(self, app_admin_class):

        app_label = app_admin_class.get_app_label()

        if app_label not in apps.app_configs:
            raise ImproperlyConfigured(
                'App with label "{}" is not registered.'.format(app_label)
            )

        if app_label in self._registry_apps.keys():
            raise AlreadyRegisteredApp(
                'In the admin already registered app with this name'.format(app_label)
            )

        app_admin = app_admin_class(self)
        self._registry_apps[app_label] = app_admin

    def get_avaliable_apps_with_models(self, request, label=None):

        avaliable_apps_with_models = dict()

        for model, admin_model in self._registry_models.items():

            model._meta.app_label

            has_module_permissions = admin_model.has_module_permissions(request)

            if not has_module_permissions:
                continue

            model_permissions = admin_model.get_model_permissions(request)

            if True not in model_permissions.values():
                continue

            app_label, model_name = model._meta.app_label, model._meta.model_name

            model_attrs = {
                'model_meta': model._meta,
                'permissions': model_permissions,
            }

            if model_permissions.get('add') is True:
                model_attrs['add_url'] = reverse(
                    'admin:{}_{}_add'.format(app_label, model_name),
                    current_app=self.name
                )

            if model_permissions.get('change') is True:
                model_attrs['changelist_url'] = reverse(
                    'admin:{}_{}_changelist'.format(app_label, model_name),
                    current_app=self.name
                )

            if app_label in avaliable_apps_with_models:
                avaliable_apps_with_models[app_label]['models'].append(model_attrs)
            else:

                app_admin = self._registry_apps.get(app_label, None)

                app_icon = getattr(app_admin, 'app_icon', 'exclamation-triangle')

                avaliable_apps_with_models[app_label] = {
                    'app_name': model._meta.app_config.verbose_name,
                    'app_index_url': reverse('admin:{}_index'.format(app_label)),
                    'app_reports_url': reverse('admin:{}_reports'.format(app_label)),
                    'app_statistics_url': reverse('admin:{}_statistics'.format(app_label)),
                    'models': [model_attrs],
                    'app_icon': app_icon,
                }

        avaliable_apps_with_models = avaliable_apps_with_models.values()

        return avaliable_apps_with_models

    def get_urls_to_active_object(self, request):

        view_class = request.resolver_match.func.view_class

        return (
            ('Home', '##'),
            ('Users', None),
        )


DefaultSiteAdmin = SiteAdmin()
