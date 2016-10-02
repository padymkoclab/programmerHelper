
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django import forms
from django.utils.html import format_html
from django.shortcuts import render, get_object_or_404
from django.db.models import NullBooleanField, BooleanField
from django.apps import apps
from django.http import HttpResponseRedirect, Http404
from django.db.models.fields.reverse_related import ManyToOneRel
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
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


class ChangeListView(SiteModelAdminMixin, generic.ListView):

    template_name = 'admin/admin/changelist.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_styles = {
            'align': 'left',
        }

    def get_queryset(self):

        return self.model_admin.get_queryset(self.request)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        model_meta = self.model_admin.model._meta

        context['title'] = _('Select {} to change').format(model_meta.verbose_name_plural.lower())

        context['model_meta'] = model_meta

        context['has_add_permission'] = self.model_admin.has_add_permission(self.request)

        context['list_display_with_styles'] = self.get_list_display_with_styles()

        context['list_values_with_styles'] = self.get_list_values_with_styles()

        return context

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

        for obj in self.get_queryset():

            values = list()
            for field_or_method in self.model_admin.get_list_display():

                if hasattr(obj, field_or_method):
                    value = getattr(obj, field_or_method)
                elif hasattr(self.model_admin, field_or_method):
                    model_admin_method = getattr(self.model_admin, field_or_method)
                    value = model_admin_method(obj)

                fieldnames = [field.name for field in self.model_admin.model._meta.get_fields()]

                # if it is not field, then it is method
                if callable(value):
                    value = value()

                elif field_or_method in fieldnames:

                    field = self.model_admin.model._meta.get_field(field_or_method)

                    if field.choices:
                        value = getattr(obj, 'get_{}_display'.format(field_or_method))()

                    if isinstance(field, (NullBooleanField, BooleanField)):

                        if value is True:
                            bootstap_class = 'ok-sign'
                            color = 'rgb(0, 255, 0)'
                        elif value is False:
                            bootstap_class = 'remove-sign'
                            color = 'rgb(255, 0, 0)'
                        elif value is None:
                            bootstap_class = 'question-sign'
                            color = 'rgb(0, 0, 0)'

                        value = format_html(
                            '<span class="glyphicon glyphicon-{}" style="color: {}"></span>',
                            bootstap_class, color
                        )

                if value is None:
                    value = self.site_admin.empty_value_display

                values.append((value, self.list_display_styles_by_column[field_or_method]))

            row_color = self.get_row_color(obj)

            admin_url = reverse('admin:{}_{}_change'.format(
                self.model_admin.model._meta.app_label,
                self.model_admin.model._meta.model_name,
            ), args=(obj.pk, ))

            list_values_with_styles.append((row_color, admin_url, values))
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

        context['model_meta'] = self.model_meta

        modelform = self.get_modelform()
        form = self.get_form()
        form.media = modelform.media
        context['form'] = form

        context['model_admin'] = self.model_admin

        return context

    def get_template_names(self):

        return [
            '{}/admin/{}/add_form.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/add_form.html'.format(self.model_meta.app_label),
            'admin/admin/add_form.html',
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

            # self.request.POST.pop('_clicked_button_save')

            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs

    def get_form(self):

        fieldsets = self.model_admin.get_fieldsets(self.request)
        return AddChangeDisplayForm(self.get_modelform(), fieldsets=fieldsets)

    def form_invalid(self, form):

        form.add_error(None, 'AAAAAAAAAAAA')

        self.add_message('invalid')

        return self.render_to_response(context=self.get_context_data(form=form))

    def form_valid(self, form):

        self.add_message('valid')

        # form.save()

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def add_message(self, status):

        if status == 'invalid':

            msg_level = messages.ERROR

            if self.obj is None:
                msg = 'Could not create an object'
            else:
                msg = 'Could not updated an object'

        if status == 'valid':

            msg_level = messages.SUCCESS

            if self.obj is None:
                msg = 'Succefully created new object'
            else:
                msg = 'Succefully updated object'

        messages.add_message(self.request, msg_level, msg)

    def get_success_url(self):

        url_info = self.model_meta.app_label, self.model_meta.model_name

        _clicked_button = self.request.POST['_clicked_button']

        if _clicked_button == 'save':
            return reverse('admin:{}_{}_changelist'.format(*url_info))
        elif _clicked_button == 'save_and_add_another':
            return reverse('admin:{}_{}_add'.format(*url_info))
        elif _clicked_button == 'save_and_continue':
            return reverse('admin:{}_{}_change'.format(*url_info), kwargs={'pk': self})


class AppIndexView(SiteAppAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/app_index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = self.app_config.verbose_name
        context['app_name'] = self.app_config.verbose_name
        context['app_models_info'] = self.get_app_models_info()
        context['reports_url'] = reverse('admin:{}_reports'.format(self.app_config.label))
        context['statistics_url'] = reverse('admin:{}_statistics'.format(self.app_config.label))

        return context

    def get_app_models_info(self):

        info = list()
        for model in self.app_config.get_models():

            info.append((
                force_text(model._meta.verbose_name),
                reverse('admin:{}_{}_changelist'.format(model._meta.app_label, model._meta.model_name)),
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

    pass


class ExportView(generic.View):

    pass


class ImportPreviewView(generic.View):

    pass


class ImportView(generic.View):

    pass


class SettingsView(SiteAdminMixin, generic.TemplateView):

    template_name = ''

    # constants
