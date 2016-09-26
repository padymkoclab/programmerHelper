
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView


class IndexView(TemplateView):

    template_name = 'admin/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['admin_site_title'] = _('programmerHelper Admin')
        context['title'] = _('Index')

        return context


class LoginView(TemplateView):

    template_name = 'admin/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['admin_site_title'] = _('programmerHelper Admin')
        context['title'] = _('Login')
        # withput labels
        # context['form'] = LoginForm

        return context


class LogoutView(TemplateView):

    template_name = 'admin/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['admin_site_title'] = _('programmerHelper Admin')
        context['title'] = _('Logout')

        return context


class PasswordChangeView(TemplateView):

    template_name = 'admin/password_change.html.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['admin_site_title'] = _('programmerHelper Admin')
        context['title'] = _('Password change')

        return context
