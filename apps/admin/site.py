
import logging

from django.conf.urls import url, include
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models.base import ModelBase
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse
from django.utils import six
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, ugettext_lazy
# from django.views.i18n import JavaScriptCatalog
# from django.template.defaultfilters import truncatechars
# from django.utils.translation import ugettext_lazy as _
# from django.contrib import admin

from .views import IndexView, LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from .decorators import admin_staff_member_required
from .admin import ModelAdmin, AppAdmin
# actions


system_check_errors = []


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AdminSite:

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
        self._registry = {}  # model_class class -> admin_class instance
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
            'available_apps': self.get_app_list(request),
        }

    def get_urls(self):
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        #
        # from django.contrib.contenttypes import views as contenttype_views

        # Admin-site-wide views.
        urlpatterns = [
            url(r'^$', IndexView, {}, 'index'),
            url(r'^login/$', LoginView, {}, 'login'),
            url(r'^logout/$', LogoutView, {}, 'logout'),
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
        for model, model_admin in self._registry.items():
            urlpatterns += [
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += [
                url(regex, admin_staff_member_required(self.app_index), name='app_list'),
            ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name

    def settings_view(self, request):
        pass

    def constants_view(self, request):
        pass

    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Registers the given model(s) with the given admin class.

        The model(s) should be Model classes, not instances.

        If an admin class isn't given, it will use ModelAdmin (the default
        admin options). If keyword arguments are given -- e.g., list_display --
        they'll be applied as options to the admin class.

        If a model is already registered, this will raise AlreadyRegistered.

        If a model is abstract, this will raise ImproperlyConfigured.
        """
        if not admin_class:
            admin_class = ModelAdmin

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    'The model %s is abstract, so it cannot be registered with admin.' % model.__name__
                )

            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            # Ignore the registration if the model has been
            # swapped out.
            if not model._meta.swapped:
                # If we got **options then dynamically construct a subclass of
                # admin_class with those **options.
                if options:
                    # For reasons I don't quite understand, without a __module__
                    # the created class appears to "live" in the wrong place,
                    # which causes issues later on.
                    options['__module__'] = __name__
                    admin_class = type("%sAdmin" % model.__name__, (admin_class,), options)

                # Instantiate the admin class to save in the registry
                admin_obj = admin_class(model, self)
                if admin_class is not ModelAdmin and settings.DEBUG:
                    system_check_errors.extend(admin_obj.check())

                self._registry[model] = admin_obj

    def unregister(self, model_or_iterable):
        """
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]

    def is_registered(self, model):
        """
        Check if a model class is registered with this `AdminSite`.
        """
        return model in self._registry

    def add_action(self, action, name=None):
        """
        Register an action to be available globally.
        """
        name = name or action.__name__
        self._actions[name] = action
        self._global_actions[name] = action

    def disable_action(self, name):
        """
        Disable a globally-registered action. Raises KeyError for invalid names.
        """
        del self._actions[name]

    def get_action(self, name):
        """
        Explicitly get a registered global action whether it's enabled or
        not. Raises KeyError for invalid names.
        """
        return self._global_actions[name]

    @property
    def actions(self):
        """
        Get all the enabled actions as an iterable of (name, func).
        """
        return six.iteritems(self._actions)

    def _build_app_dict(self, request, label=None):
        """
        Builds the app dictionary. Takes an optional label parameters to filter
        models of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                if label:
                    raise PermissionDenied
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
            }
            if perms.get('change'):
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Returns a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list

    def app_index(self, request, app_label, extra_context=None):
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

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)


# This global object represents the default admin site, for the common case.
# You can instantiate AdminSite in your own code to create a custom admin site.
admin_site = AdminSite()
