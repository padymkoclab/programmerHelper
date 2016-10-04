
import collections

from django.contrib import messages
from django import forms
# from django.contrib.admin.checks import ModelAdminChecks
from django.conf.urls import url
from django.contrib.auth import get_permission_codename
# from django.urls import reverse
# from django.utils.encoding import force_text
# from django.utils.html import escape, format_html
# from django.utils.safestring import mark_safe
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext_lazy as _, ungettext
# from django.views.decorators.csrf import csrf_protect
# from django.views.generic import RedirectView

from utils.python.utils import flatten

from .forms import AddChangeModelForm
from .decorators import admin_staff_member_required
from .views import AddView, ChangeListView, ChangeView, HistoryView, DeleteView


class CheckModelAdmin:

    def check(self, admin_obj):

        errors = []

        # from django.views.generic import View

        # if not isinstance(admin_obj.changelist_view, View):
        #     raise ValueError('Model admin class must be passed changelist_view as CBV')
        #
        return errors


class ModelAdmin:

    # raw_id_fields = ()
    # exclude = None
    # filter_vertical = ()
    # filter_horizontal = ()
    # radio_fields = {}
    # formfield_overrides = {}
    readonly_fields = ()
    # view_on_site = True
    # show_full_result_count = True

    form = AddChangeModelForm
    list_display = ('__str__', )
    list_display_styles = (
        (
            '__all__', {
                'align': 'center',
            }
        ),
    )
    colored_rows_by = ''
    ordering = ()
    disabled_urls = ()
    prepopulated_fields = {}
    fields = ()
    fieldsets = ()

    # list_display_links = ()
    # list_filter = ()
    # list_select_related = False
    list_per_page = 100
    # list_max_show_all = 200
    # list_editable = ()
    search_fields = ()
    # date_hierarchy = None
    # save_as = False
    # save_as_continue = True
    # save_on_top = False
    # paginator = Paginator
    # preserve_filters = True
    # inlines = []

    # # Custom templates (designed to be over-ridden in subclasses)
    # add_form_template = None
    # change_form_template = None
    # change_list_template = None
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None

    # # Actions
    actions = ()
    # action_form = helpers.ActionForm
    # actions_on_top = True
    # actions_on_bottom = False
    # actions_selection_counter = True
    checks_class = CheckModelAdmin

    # views
    changelist_view = None

    def __init__(self, model, site_admin, **kwargs):
        self.model = model
        self.site_admin = site_admin

    def __str__(self):
        return 'Admin model class "{}" for a model "{}"'.format(self.__class__.__name__, self.model)

    def check(self, **kwargs):
        return self.checks_class().check(self, **kwargs)

    def get_urls(self):

        info = self.model._meta.app_label, self.model._meta.model_name

        urls = dict(
            changelist=url(
                regex=r'^$', kwargs={}, name='{}_{}_changelist'.format(*info),
                view=admin_staff_member_required(
                    ChangeListView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            add=url(
                regex=r'^add/$', kwargs={}, name='{}_{}_add'.format(*info),
                view=admin_staff_member_required(
                    AddView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            change=url(
                regex=r'^(?P<pk>.+)/change/$', name='{}_{}_change'.format(*info), kwargs={},
                view=admin_staff_member_required(
                    ChangeView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            history=url(
                regex=r'^(?P<pk>.+)/history/$', name='{}_{}_history'.format(*info), kwargs={},
                view=admin_staff_member_required(
                    HistoryView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            delete=url(
                regex=r'^(?P<pk>.+)/delete/$', name='{}_{}_delete'.format(*info), kwargs={},
                view=admin_staff_member_required(
                    DeleteView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
        )

        urlpatterns = [url for url_name, url in urls.items() if url_name not in self.disabled_urls]

        # url(r'^(.+)/preview/$', wrap(self.change_view), name='%s_%s_preview' % info),
        # url(r'^(.+)/statistics/$', wrap(self.change_view), name='%s_%s_statistics' % info),
        # url(r'^(.+)/reports/$', wrap(self.change_view), name='%s_%s_reports' % info),

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        ordering = self.get_ordering()

        if ordering:
            qs.order_by(*ordering)

        return qs

    def get_ordering(self):

        return self.ordering

    def get_list_display(self):

        return self.list_display

    def has_module_permissions(self, request):

        return request.user.has_module_permissions(self.model._meta.app_label)

    def get_model_permissions(self, request):

        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
        }

    def has_add_permission(self, request):

        permission_codename = get_permission_codename('add', self.model._meta)
        permission = '{}.{}'.format(self.model._meta.app_label, permission_codename)
        return request.user.has_permission(permission)

    def has_change_permission(self, request):

        permission_codename = get_permission_codename('change', self.model._meta)
        permission = '{}.{}'.format(self.model._meta.app_label, permission_codename)
        return request.user.has_permission(permission)

    def has_delete_permission(self, request):

        permission_codename = get_permission_codename('delete', self.model._meta)
        permission = '{}.{}'.format(self.model._meta.app_label, permission_codename)
        return request.user.has_permission(permission)

    def get_list_display_styles(self):

        return self.list_display_styles

    def get_colored_rows_by(self):

        return self.colored_rows_by

    def get_prepopulated_fields(self):

        return self.prepopulated_fields

    def get_fields(self, request, obj=None):

        return self.fields or ()

    def get_fieldsets(self, request, obj=None):

        if self.fieldsets:
            return self.fieldsets

        return (
            (
                None, {
                    'fields': self.get_fields(request, obj),
                }
            ),
        )

    def get_form(self, request):

        fields = self.get_fields(request)
        fieldsets = self.get_fieldsets(request)

        if not fields:
            fields = tuple(flatten([options['fields'] for label, options in fieldsets]))

        if not fields:
            fields = forms.ALL_FIELDS

        return forms.models.modelform_factory(self.model, fields=fields, form=self.form)

    def get_search_fields(self):

        return self.search_fields

    def get_actions(self):

        global_actions = self.site_admin.actions

        local_actions = dict()
        if self.actions:
            for action in self.actions:

                action = action if callable(action) else getattr(self.model_admin, action)

                local_actions[action.__name__] = action

        global_actions.update(local_actions)

        actions = collections.OrderedDict()

        for name, func in global_actions.items():

            if hasattr(func, 'short_description'):
                description = func.short_description
                description = description.format(self.model._meta.verbose_name_plural.lower())
            else:
                description = name.replace('_', ' ')
                description = capfirst(description)
                description = '{} {}'.format(description, self.model._meta.verbose_name_plural.lower())

            actions[name] = dict(func=func, description=description)

        return actions

    def message_user(self, request, msg, level=messages.INFO, extra_tags='', fail_silently=False):

        if isinstance(level, str):
            level = messages.DEFAULT_LEVELS[level]

        messages.add_message(request, level, msg, extra_tags, fail_silently)

    def get_readonly_fields(self, request, obj=None):

        return self.readonly_fields


class OtherAdmin:

    pass


class StackedInline:
    template = 'admin/edit_inline/stacked.html'


class TabularInline:
    template = 'admin/edit_inline/tabular.html'


class TableInline:
    template = 'admin/edit_inline/table.html'
