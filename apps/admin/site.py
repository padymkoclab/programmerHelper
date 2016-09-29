
import logging

from django.core.urlresolvers import reverse
from django.conf.urls import url, include
# from django.apps import apps
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

from .views import IndexView, LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from .decorators import admin_staff_member_required
from .admin import ModelAdmin, AppAdmin
# actions


logging = logging.getLogger('django.development')


system_check_errors = []


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


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
        self._registry_app = {}
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
            'title': 'ERRRROR',
            'admin_site_header': self.admin_site_header,
            # 'site_url': site_url,
            'has_permission': self.has_permission(request),
            'avaliable_apps_models': self.get_avaliable_apps_models(request),
        }

    def get_urls(self):
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        #
        # from django.contrib.contenttypes import views as contenttype_views

        # Admin-site-wide views.

        # PasswordChangeView = admin_staff_member_required(PasswordChangeView.as_view(), cacheable=True)
        # PasswordChangeDoneView = admin_staff_member_required(PasswordChangeDoneView.as_view(), cacheable=True)

        urlpatterns = [
            url(r'^$', admin_staff_member_required(IndexView.as_view(site_admin=self)), {}, 'index'),
            url(r'^login/$', csrf_protect(never_cache(LoginView.as_view())), {}, 'login'),
            url(r'^logout/$', admin_staff_member_required(LogoutView.as_view()), {}, 'logout'),
            url(r'^password_change/$', PasswordChangeView, {}, 'password_change'),
            url(r'^password_change/done/$', PasswordChangeDoneView, {}, 'password_change_done'),
            # url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
            #
            # app:
            #   changelist
            #   change
            #   preview
            #   delete
            #   history
            #   statistics
            #   reports
            #
            # site:
            #   settings
            #   constants
        ]

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []

        # import ipdb; ipdb.set_trace()

        for model, model_admin in self._registry_models.items():
            urlpatterns += [
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        #
        # if valid_app_labels:
        #     regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
        #     urlpatterns += [
        #         url(regex, admin_staff_member_required(self.app_index), name='app_list'),
        #     ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name

    def settings_view(self, request):
        pass

    def constants_view(self, request):
        pass

    def register_model(self, model, model_admin_class):
        """
        """

        if model._meta.abstract:
            raise ImproperlyConfigured(
                'The model {} is abstract, so it cannot be registered with admin.'.format(model._meta.model_name)
            )

        if model in self._registry_models:
            raise AlreadyRegistered('The model {} is already registered'.format(model._meta.model_name))

        # Ignore the registration if the model has been
        # swapped out.
        if not model._meta.swapped:

            # Instantiate the admin class to save in the registry
            model_admin = model_admin_class(model, self)
            if model_admin_class is not ModelAdmin and settings.DEBUG:
                system_check_errors.extend(model_admin.check())

            self._registry_models[model] = model_admin

    def get_avaliable_apps_models(self, request, label=None):

        avaliable_apps_models = dict()

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
                'name': model._meta.verbose_name_plural,
                'permissions': model_permissions,
                'object_name': model._meta.object_name,
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

            if app_label in avaliable_apps_models:
                avaliable_apps_models[app_label]['models'].append(model_attrs)
            else:
                avaliable_apps_models[app_label] = {
                    'name': model._meta.app_config.verbose_name,
                    'models': [model_attrs],
                    'app_index_url': '#',
                }

        avaliable_apps_models = avaliable_apps_models.values()

        return avaliable_apps_models


DefaultSiteAdmin = SiteAdmin()
