
from django.db.models.fields.reverse_related import ManyToOneRel
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.contrib.auth import login, logout
from django.utils.text import capfirst, force_text

from .forms import LoginForm
from .descriptors import SiteAdminStrictDescriptor, ModelAdminStrictDescriptor


class IndexView(generic.TemplateView):

    template_name = 'admin/admin/index.html'
    site_admin = SiteAdminStrictDescriptor('site_admin')

    def __init__(self, site_admin, *args, **kwargs):

        self.site_admin = site_admin

        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.site_admin.each_context(self.request))

        context['title'] = _('Index')

        return context


class LoginView(generic.FormView):

    template_name = 'admin/admin/login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('Login')

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


class ChangeListView(generic.ListView):

    template_name = 'admin/admin/changelist.html'

    model_admin = ModelAdminStrictDescriptor('model_admin')
    site_admin = SiteAdminStrictDescriptor('site_admin')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = _('Select {} to change').format(
            self.model_admin.model._meta.verbose_name_plural.lower()
        )

        self.default_classes = {
            'align': 'left',
        }

    def get_queryset(self):

        return self.model_admin.get_queryset(self.request)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update(self.site_admin.each_context(self.request))

        context['title'] = self.title

        context['model_meta'] = self.model_admin.model._meta

        context['model_name'] = self.model_admin.model._meta.verbose_name_plural

        context['has_add_permission'] = self.model_admin.has_add_permission(self.request)

        context['list_display_with_classes'] = self.get_list_display_with_classes()

        context['list_values_with_classes'] = self.get_list_values_with_classes()

        return context

    @property
    def list_display_classes_by_column(self):

        columns_with_classes = {}

        for field_or_method in self.model_admin.get_list_display():

            current_list_display_classes = [
                styles for fields, styles in self.model_admin.get_list_display_classes()
                if field_or_method in fields
            ]

            current_list_display_classes = current_list_display_classes[0]

            classes = self.default_classes.copy()

            classes.update(current_list_display_classes)

            columns_with_classes[field_or_method] = classes

        return columns_with_classes


    def get_list_values_with_classes(self):

        list_values_with_classes = list()

        for obj in self.get_queryset():

            values = list()
            for field_or_method in self.model_admin.get_list_display():

                value = getattr(obj, field_or_method)

                fieldnames = [field.name for field in self.model_admin.model._meta.get_fields()]

                # if it is not field, then it is method
                if callable(value):
                    value = value()

                elif field_or_method in fieldnames:

                    field = self.model_admin.model._meta.get_field(field_or_method)
                    if field.choices:
                        value = getattr(obj, 'get_{}_display'.format(field_or_method))()

                if value is None:
                    value = self.site_admin.empty_value_display

                values.append((value, self.list_display_classes_by_column[field_or_method]))

            row_color = self.get_row_color(obj)

            admin_url = reverse('admin:{}_{}_change'.format(
                self.model_admin.model._meta.app_label,
                self.model_admin.model._meta.model_name,
            ), args=(obj.pk, ))

            list_values_with_classes.append((row_color, admin_url, values))
        return list_values_with_classes

    def get_list_display_with_classes(self):

        list_display = self.model_admin.get_list_display()

        new_list_display = list()

        for name_attr_display in list_display:

            # made also __all__
            if name_attr_display == '__str__':

                attr_display = self.model_admin.model._meta.verbose_name

            else:

                attr_display = getattr(self.model_admin.model, name_attr_display)

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

            new_list_display.append((attr_display, self.list_display_classes_by_column[name_attr_display]))

        return new_list_display

    def get_row_color(self, obj):

        colored_rows_by = self.model_admin.get_colored_rows_by()

        row_color = None
        if hasattr(self.model_admin, colored_rows_by):

            colored_rows_by = getattr(self.model_admin, colored_rows_by)
            if callable(colored_rows_by):
                row_color = colored_rows_by(obj)

        return row_color


class AddView(generic.CreateView):

    model_admin = ModelAdminStrictDescriptor('model_admin')
    site_admin = SiteAdminStrictDescriptor('site_admin')


class ChangeView(generic.UpdateView):

    model_admin = ModelAdminStrictDescriptor('model_admin')
    site_admin = SiteAdminStrictDescriptor('site_admin')
