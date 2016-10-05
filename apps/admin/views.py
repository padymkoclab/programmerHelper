
from django.http.request import QueryDict
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django import forms
from django.utils.html import format_html
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.apps import apps
from django.http import HttpResponseRedirect, Http404
from django.db.models.fields.reverse_related import ManyToOneRel
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _, ungettext
from django.views import generic
from django.contrib.auth import login, logout
from django.utils.text import capfirst, force_text

from utils.django.views_mixins import ContextTitleMixin

from .forms import LoginForm, AddChangeDisplayForm
from .descriptors import SiteAdminStrictDescriptor, ModelAdminStrictDescriptor
from .views_mixins import SiteAdminMixin, SiteModelAdminMixin, SiteAppAdminMixin, ContextAdminMixin


class IndexView(SiteAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/index.html'
    title = _('Index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(ContextTitleMixin, generic.FormView):

    template_name = 'admin/admin/login.html'
    form_class = LoginForm
    title = _('Login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        login(self.request, form.get_user())

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:index')


class LogoutView(generic.RedirectView):

    pattern_name = 'admin:login'
    permament = False

    def get_redirect_url(self, *args, **kwargs):

        logout(self.request)

        return super().get_redirect_url(*args, **kwargs)


class PasswordChangeView(generic.TemplateView):

    template_name = 'admin/admin/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.site_admin.each_context(self.request))

        context['title'] = _('Password change')

        return context


class PasswordChangeDoneView(generic.TemplateView):

    pass


class ChangeListView(SiteModelAdminMixin, generic.View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_meta = self.model_admin.model._meta

        self.default_styles = {
            'align': 'left',
        }

        self.list_per_page = self.model_admin.list_per_page

    def post(self, request):

        pks_selected_objects = request.POST.getlist('selected_objects')
        queryset = self.model_admin.model._default_manager.filter(pk__in=pks_selected_objects)

        if not queryset.exists():

            messages.add_message(
                request, messages.WARNING,
                "Items must be selected in order to perform actions on them. No items have been changed.",
                extra_tags='warning'
            )

            return self.render_to_response(request)

        action = request.POST.get('action')

        actions = self.model_admin.get_actions()

        # get function of action
        func = actions[action]['func']

        # make action
        func(self.model_admin, request, queryset)

        return self.render_to_response(request)

    def get(self, request):

        return self.render_to_response(request)

    def get_queryset(self, request):

        qs = self.model_admin.get_queryset(request)

        search_fields = self.model_admin.get_search_fields()

        if search_fields:

            if self.q and search_fields:

                if self.type_search not in ('contains', 'startswith', 'endswith'):
                    raise ValueError('Not correct value of "type_search".')

                # convert ignorecase to the Django`s lookup type
                self.ignorecase = '' if self.ignorecase is None else 'i'

                # make a lookup format for the search
                lookup = '__{}{}'.format(self.ignorecase, self.type_search)

                # make the same conditions for each field in the search_fields
                conditions = {'{}{}'.format(field, lookup): self.q for field in search_fields}

                # filter by conditions on the all fields listed the search_fields
                qs = qs.filter(**conditions)

                count = qs.count()

                object_name = self.model_meta.verbose_name if count == 1 else self.model_meta.verbose_name_plural
                object_name = object_name.lower()

                msg = ungettext(
                    'By a condition "{}" found {} {}',
                    'By a condition "{}" found {} {}',
                    count
                ).format(self.q, count, object_name)

                self.model_admin.message_user(request, msg, extra_tags='info', level='INFO')

        return qs

    def get_context_data(self, **kwargs):

        context = self.site_admin.each_context(self.request)

        self.q = self.request.GET.get('q', '')
        self.q = self.q.strip()
        self.ignorecase = self.request.GET.get('ignorecase', '1')
        self.type_search = self.request.GET.get('type_search', 'contains')

        context['title'] = _('Select {} to change').format(self.model_meta.verbose_name_plural.lower())

        context['model_meta'] = self.model_meta
        context['model_admin'] = self.model_admin

        context['q'] = self.q
        context['ignorecase'] = self.ignorecase
        context['type_search'] = self.type_search

        listing_search_fields = [
            force_text(self.model_meta.get_field(field).verbose_name)
            for field in self.model_admin.search_fields
        ]
        context['listing_search_fields'] = ', '.join(listing_search_fields)

        context['has_add_permission'] = self.model_admin.has_add_permission(self.request)
        context['has_export_permission'] = self.model_admin.has_add_permission(self.request)
        context['has_import_permission'] = self.model_admin.has_add_permission(self.request)

        list_values_with_styles = self.get_list_values_with_styles()

        list_per_page = self.request.GET.get('list_per_page', self.list_per_page)
        list_per_page = int(list_per_page)

        paginator = Paginator(list_values_with_styles, list_per_page)
        total_count_objects = paginator.count

        page = self.request.GET.get('page')

        try:
            page_object_list = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_object_list = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_object_list = paginator.page(page)

        context['page_object_list'] = page_object_list
        context['total_count_objects'] = total_count_objects

        list_per_page = total_count_objects if total_count_objects < list_per_page else list_per_page

        context['list_per_page'] = list_per_page

        context['list_display_with_styles'] = self.get_list_display_with_styles()

        context['actions'] = self.model_admin.get_actions()

        return context

    def render_to_response(self, request):

        return TemplateResponse(
            request,
            template=self.get_template_names(),
            context=self.get_context_data()
        )

    def get_template_names(self):

        return [
            '{}/admin/{}/admin/changelist.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/admin/changelist.html'.format(self.model_meta.app_label),
            'admin/admin/changelist.html',
        ]

    @property
    def list_display_styles_by_column(self):

        columns_with_styles = {}

        styles_by_column = {
            column: styles
            for columns, styles in self.model_admin.get_list_display_styles()
            for column in columns
        }

        global_styles = styles_by_column.pop('__all__') if '__all__' in styles_by_column else dict()

        list_display_dict = dict.fromkeys(self.model_admin.get_list_display(), {})

        for column, styles in list_display_dict.items():

            value = self.default_styles.copy()
            value.update(global_styles)
            value.update(styles_by_column.get(column, {}))
            columns_with_styles[column] = value

        return columns_with_styles

    def get_list_values_with_styles(self):

        list_values_with_styles = list()

        for obj in self.get_queryset(self.request):

            values = list()
            for field_or_method in self.model_admin.get_list_display():

                if hasattr(obj, field_or_method):
                    value = getattr(obj, field_or_method)
                elif hasattr(self.model_admin, field_or_method):
                    model_admin_method = getattr(self.model_admin, field_or_method)
                    value = model_admin_method(obj)
                else:
                    raise Exception(field_or_method)

                fieldnames = [field.name for field in self.model_admin.model._meta.get_fields()]

                # if it is not field, then it is method
                if callable(value):

                    if hasattr(value, 'boolean'):
                        value = value()
                        value = self.convert_boolean_to_bootstrap_icon(value)
                    else:
                        value = value()

                elif field_or_method in fieldnames:

                    field = self.model_admin.model._meta.get_field(field_or_method)

                    if field.choices:
                        value = getattr(obj, 'get_{}_display'.format(field_or_method))()

                    if isinstance(field, (models.NullBooleanField, models.BooleanField)):
                        value = self.convert_boolean_to_bootstrap_icon(value)

                if value is None:
                    value = self.site_admin.empty_value_display

                values.append((value, self.list_display_styles_by_column[field_or_method]))

            row_color = self.get_row_color(obj)

            admin_url = self.site_admin.get_url('change', self.model_meta, kwargs={'pk': obj.pk})

            list_values_with_styles.append((row_color, admin_url, obj.pk, values))
        return list_values_with_styles

    def get_list_display_with_styles(self):

        list_display = self.model_admin.get_list_display()

        new_list_display = list()

        for name_attr_display in list_display:

            # made also __all__
            if name_attr_display == '__str__':

                attr_display = self.model_admin.model._meta.verbose_name

            else:

                if hasattr(self.model_admin.model, name_attr_display):
                    attr_display = getattr(self.model_admin.model, name_attr_display)
                elif hasattr(self.model_admin, name_attr_display):
                    attr_display = getattr(self.model_admin, name_attr_display)
                else:
                    raise AttributeError(
                        'Either no model or model admin has no attribute {}'.format(
                            name_attr_display
                        )
                    )

                if callable(attr_display):

                    if hasattr(attr_display, 'short_description'):
                        attr_display = force_text(attr_display.short_description)
                    else:
                        attr_display = attr_display.__name__.replace('_', ' ')
                        attr_display = force_text(attr_display)
                        attr_display = capfirst(attr_display)

                elif isinstance(attr_display, property):

                    attr_display = attr_display.fget.__name__.replace('_', ' ')
                    attr_display = force_text(attr_display)
                    attr_display = capfirst(attr_display)

                else:

                    field = self.model_admin.model._meta.get_field(name_attr_display)

                    if isinstance(field, ManyToOneRel):
                        raise TypeError(
                            'Does not support for field ({}) with type ManyToOneRel.'.format(field.name)
                        )

                    attr_display = field.verbose_name

            new_list_display.append((attr_display, self.list_display_styles_by_column[name_attr_display]))

        return new_list_display

    def get_row_color(self, obj):

        colored_rows_by = self.model_admin.get_colored_rows_by()

        row_color = None
        if hasattr(self.model_admin, colored_rows_by):

            colored_rows_by = getattr(self.model_admin, colored_rows_by)
            if callable(colored_rows_by):
                row_color = colored_rows_by(obj)

        return row_color

    @staticmethod
    def convert_boolean_to_bootstrap_icon(value):

        if value is True:
            bootstap_class = 'ok-sign'
            color = 'rgb(0, 255, 0)'
        elif value is False:
            bootstap_class = 'remove-sign'
            color = 'rgb(255, 0, 0)'
        elif value is None:
            bootstap_class = 'question-sign'
            color = 'rgb(0, 0, 0)'

        return format_html(
            '<span class="glyphicon glyphicon-{}" style="color: {}"></span>',
            bootstap_class, color
        )


class AddView(SiteModelAdminMixin, generic.View):

    def dispatch(self, request, *args, **kwargs):

        if not self.model_admin.has_change_permission(request):
            raise PermissionDenied

        return AddChangeView.as_view(model_admin=self.model_admin, site_admin=self.site_admin)(request)


class ChangeView(SiteModelAdminMixin, generic.View):

    def dispatch(self, request, *args, **kwargs):

        if not self.model_admin.has_change_permission(request):
            raise PermissionDenied

        pk = kwargs['pk']

        # get_object_or_404 does not working with UUID
        try:
            obj = self.model_admin.model._default_manager.get(pk=pk)
        except (self.model_admin.model.DoesNotExist, ValueError):
            raise Http404(_('An object doesn`t found'))

        return AddChangeView.as_view(model_admin=self.model_admin, site_admin=self.site_admin)(request, obj)


class AddChangeView(ContextAdminMixin, generic.FormView):

    model_admin = None
    site_admin = None

    def __init__(self, model_admin, site_admin, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_admin = model_admin
        self.site_admin = site_admin

        self.model_meta = self.model_admin.model._meta

    def dispatch(self, request, obj=None, *args, **kwargs):

        self.obj = obj

        return super().dispatch(request, *args, **kwargs)

    def get_title(self):

        if self.obj is not None:
            return _('Change {} "{}"').format(
                self.model_meta.verbose_name.lower(), self.obj
            )
        return _('Add {}').format(self.model_meta.verbose_name.lower())

    def get_context_data(self, **kwargs):

        context = super().get_context_data()

        context['title'] = self.get_title()

        context['object'] = self.obj

        context['has_delete_permission'] = self.model_admin.has_delete_permission(self.request)

        context['model_meta'] = self.model_meta

        modelform = self.get_modelform()
        form = self.get_form()
        form.media = modelform.media
        context['form'] = form

        context['model_admin'] = self.model_admin

        return context

    def get_template_names(self):

        return [
            '{}/admin/{}/addchange_form.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/addchange_form.html'.format(self.model_meta.app_label),
            'admin/admin/addchange_form.html',
        ]

    def post(self, request):

        form = self.get_modelform()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_class(self):

        return self.model_admin.get_form(self.request)

    def get_modelform(self):

        form = self.get_form_class()
        return form(instance=self.obj, **self.get_form_kwargs())

    def get_initial(self):

        if self.obj is None:
            return {}
        field_names = [i for i in self.get_form_class().base_fields]

        return {fieldname: getattr(self.obj, fieldname) for fieldname in field_names}

    def get_form_kwargs(self):

        kwargs = dict(initial=self.get_initial())

        if self.request.method == 'POST':

            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs

    def get_form(self):

        return AddChangeDisplayForm(
            self.get_modelform(),
            fieldsets=self.model_admin.get_fieldsets(self.request, self.obj),
            readonly_fields=self.model_admin.get_readonly_fields(self.request, self.obj),
            model_admin=self.model_admin,
        )

    def form_invalid(self, form):

        object_name = self.model_meta.verbose_name.lower()

        if self.obj is None:
            msg = _('Could not create a new {}').format(object_name)
        else:
            msg = _('Could not update the {} "{}"').format(object_name, self.obj)

        self.model_admin.message_user(self.request, msg, 'ERROR', 'error')

        return self.render_to_response(context=self.get_context_data(form=form))

    def form_valid(self, form):

        self.object = form.save(commit=False)

        self.object.save()

        object_name = self.model_meta.verbose_name.lower()

        if self.obj is None:
            extra_tags = 'created'
            msg = _('Succefully created new {} "{}"').format(object_name, self.object)
        else:
            extra_tags = 'updated'
            msg = _('Succefully updated {} "{}"').format(object_name, self.object)

        self.model_admin.message_user(self.request, msg, 'SUCCESS', extra_tags)

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_success_url(self):

        _clicked_button = self.request.POST['_clicked_button']

        if _clicked_button == 'save':
            return self.site_admin.get_url('changelist', self.model_meta)
        elif _clicked_button == 'save_and_add_another':
            return self.site_admin.get_url('add', self.model_meta)
        elif _clicked_button == 'save_and_continue':
            return self.site_admin.get_url('change', self.model_meta, kwargs={'pk': self.object.pk})


class AppIndexView(SiteAppAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/app_index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = self.app_config.verbose_name
        context['app_name'] = self.app_config.verbose_name
        context['app_models_info'] = self.get_app_models_info()
        context['reports_url'] = self.site_admin.get_url('reports', self.app_config.label)
        context['statistics_url'] = self.site_admin.get_url('statistics', self.app_config.label)

        return context

    def get_app_models_info(self):

        info = list()
        for model in self.app_config.get_models():

            if self.site_admin.is_registered_model(model):
                info.append((
                    force_text(model._meta.verbose_name),
                    self.site_admin.get_url('changelist', model._meta),
                    model._default_manager.count(),
                ))

        info.sort(key=lambda x: x[0].lower())

        return info


class AppReportView(SiteAppAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('{} - Reports ').format(self.app_config.verbose_name)

        context['app_name'] = self.app_config.verbose_name

        return context


class AppStatisticsView(SiteAppAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('{} - Statistics ').format(self.app_config.verbose_name)

        context['app_name'] = self.app_config.verbose_name

        return context


class HistoryView(SiteModelAdminMixin, generic.DetailView):

    pass


class DeleteView(SiteModelAdminMixin, generic.DeleteView):

    pk_url_kwarg = 'pk'
    context_object_name = 'object'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = self.model_admin.model
        self.model_meta = self.model._meta

    def dispatch(self, request, *args, **kwargs):

        if not self.model_admin.has_delete_permission(request):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):

        return [
            '{}/admin/{}/confirm_delete.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/confirm_delete.html'.format(self.model_meta.app_label),
            'admin/admin/confirm_delete.html',
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_meta'] = self.model_meta
        context['related_objects'] = self.get_related_objects()
        context['title'] = _('Delete {}').format(
            self.model_meta.verbose_name.lower()
        )

        return context

    def get_success_url(self):

        return self.site_admin.get_url('changelist', self.model_meta)

    def get_related_objects(self):

        related_objects = list()

        candidate_relations_to_delete = [
            i for i in self.object._meta.get_fields(include_hidden=True)
            if i.auto_created and not i.concrete and (i.one_to_one or i.one_to_many)
        ]

        for relationship in candidate_relations_to_delete:
            if relationship.on_delete != models.DO_NOTHING:

                related_model = relationship.related_model
                type_relationship = relationship.on_delete.__name__
                objects = related_model._base_manager.filter(
                    **{'{}__in'.format(
                        relationship.field.name): [self.object.pk]}
                )

                related_objects.append(
                    (related_model._meta, type_relationship, objects)
                )

        return related_objects

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        messages.add_message(
            request,
            messages.SUCCESS,
            _('Successfully deleted {} "{}"').format(self.model_meta.verbose_name.lower(), self.object),
            extra_tags='deleted',

        )

        return HttpResponseRedirect(success_url)


class ExportView(generic.View):

    pass


class ImportPreviewView(generic.View):

    pass


class ImportView(generic.View):

    pass


class SettingsView(SiteAdminMixin, generic.TemplateView):

    template_name = ''

    # constants
