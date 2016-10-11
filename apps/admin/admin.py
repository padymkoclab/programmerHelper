
import functools
import logging
import collections

from django.contrib import messages
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.db import models
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
from .widgets import RelatedFieldWidgetWrapper
from .decorators import admin_staff_member_required
from .views import AddView, ChangeListView, ChangeView, HistoryView, DeleteView


logger = logging.getLogger('django.development')


class CheckModelAdmin:

    def check(self, admin_obj):

        errors = []

        # from django.views.generic import View

        # if not isinstance(admin_obj.changelist_view, View):
        #     raise ValueError('Model admin class must be passed changelist_view as CBV')
        #
        return errors


class BaseAdmin(object):

    raw_id_fields = ()
    exclude = None
    filter_vertical = ()
    filter_horizontal = ()
    radio_fields = {}
    formfield_overrides = {}
    readonly_fields = ()
    view_on_site = True
    form = forms.ModelForm
    ordering = ()
    prepopulated_fields = {}
    fields = ()
    fieldsets = ()

    def get_ordering(self):

        return self.ordering

    def get_prepopulated_fields(self):

        return self.prepopulated_fields

    def get_fields(self, request, obj=None):

        return self.fields or ()

    def get_readonly_fields(self, request, obj=None):

        return self.readonly_fields

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        ordering = self.get_ordering()

        if ordering:
            qs.order_by(*ordering)

        return qs

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


class ModelAdmin(BaseAdmin):

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

    list_display_links = ()
    list_filter = ()
    list_per_page = 100
    search_fields = ()
    date_hierarchy = None
    inlines = []

    # Custom templates (designed to be over-ridden in subclasses)
    # add_form_template = None
    # change_form_template = None
    # change_list_template = None
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None

    # Actions
    actions = ()
    # action_form = helpers.ActionForm
    # actions_on_top = True
    # actions_on_bottom = False
    actions_selection_counter = True
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

    def get_list_display(self):

        return self.list_display

    def has_module_permissions(self, request):

        return request.user.has_module_permissions(self.model._meta.app_label)

    def get_model_permissions(self, request):

        logger.info('New permission: make reports, export/import data')

        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
        }

    def get_list_display_styles(self):

        return self.list_display_styles

    def get_colored_rows_by(self):

        return self.colored_rows_by

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

        return forms.models.modelform_factory(
            self.model,
            fields=fields,
            form=self.form,
            formfield_callback=functools.partial(self.override_admin_formfield, request=request)
        )

    def override_admin_formfield(self, db_field, request, **kwargs):

        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):

            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)

            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            formfield.widget = RelatedFieldWidgetWrapper(formfield.widget, db_field, self.site_admin)

            return formfield

        return db_field.formfield(**kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # if 'queryset' not in kwargs:
        #     queryset =
        #     kwargs['kwargs'] = queryset

        return db_field.formfield(**kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        return db_field.formfield(**kwargs)

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

    def get_list_filter(self, request):

        return self.list_filter

    def get_inline_instances(self, request, obj=None):

        # make premission check here
        return [inline(self.model, self.site_admin) for inline in self.inlines]

    def get_inlines_formsets(self, request, obj):

        inlines_formsets = list()
        for inline in self.get_inline_instances(request, obj):
            inline_formset = inline.get_formset(request, obj)

            params = {
                'instance': obj,
                'queryset': inline.get_queryset(request),
            }

            if request.method == 'POST':
                params.update({
                    'data': request.POST,
                    'files': request.FILES,
                })

            formset = inline_formset(**params)

            inlines_formsets.append((inline, formset))

        return inlines_formsets


class AdminInline(BaseAdmin):

    model = None
    fk_name = None
    template = None
    verbose_name = None
    verbose_name_plural = None
    can_delete = True
    show_change_link = True
    min_num = None
    max_num = None
    formset = BaseInlineFormSet
    extra = 3
    classes = None
    form = forms.ModelForm

    def __init__(self, parent_model, site_admin, *args, **kwargs):
        self.parent_model = parent_model
        self.site_admin = site_admin
        self.model_meta = self.model._meta
        self.verbose_name = self.model_meta.verbose_name if self.verbose_name is None else self.verbose_name
        self.verbose_name_plural = self.model_meta.verbose_name_plural\
            if self.verbose_name_plural is None else self.verbose_name_plural

    def get_extra(self, request, obj=None, **kwargs):

        return self.extra

    def get_min_num(self, request, obj=None, **kwargs):

        return self.min_num

    def get_max_num(self, request, obj=None, **kwargs):

        return self.max_num

    def get_formset(self, request, obj=None, **kwargs):

        fields = self.get_fields(request, obj)

        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)

        readonly_fields = self.get_readonly_fields(request, obj)
        exclude.extend(readonly_fields)

        params = {
            'form': self.form,
            'formset': self.formset,
            'fields': fields,
            'exclude': exclude,
            'fk_name': self.fk_name,
            'min_num': self.get_min_num(request, obj),
            'max_num': self.get_max_num(request, obj),
            'extra': self.get_extra(request, obj),
        }
        params.update(kwargs)

        if not params['fields']:
            params['fields'] = forms.ALL_FIELDS

        return inlineformset_factory(self.parent_model, self.model, **params)

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if self.has_change_permission(request):
            return qs
        return qs.none()

    def has_add_permission(self, request):

        if self.model_meta.auto_created:
            # if is Intermediate model (ManyToManyField) verify only permission on change object
            return self.has_change_permission(request)

        return super().has_add_permission(request)

    def has_change_permission(self, request):

        if self.model_meta.auto_created:
            for field in self.model_meta.fields:
                # if field.remote_field
                raise Exception

        return super().has_change_permission(request)

    def has_delete_permission(self, request):

        if self.model_meta.auto_created:
            # if is Intermediate model (ManyToManyField) verify only permission on change object
            return self.has_change_permission(request)

        return super().has_delete_permission(request)


class StackedInline(AdminInline):
    template = 'admin/admin/edit_inline/stacked.html'


class TabularInline(AdminInline):
    template = 'admin/admin/edit_inline/tabular.html'


class OtherAdmin:

    pass
