
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView, FormView, RedirectView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout

from .forms import LoginForm
from .decorators import admin_staff_member_required


class IndexView(TemplateView):

    template_name = 'admin/admin/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # each_context(self.request, context)

        context['title'] = _('Index')

        return context


class LoginView(FormView):

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


class LogoutView(RedirectView):

    pattern_name = 'admin:login'
    permament = False

    def get_redirect_url(self, *args, **kwargs):

        logout(self.request)

        return super().get_redirect_url(*args, **kwargs)


class PasswordChangeView(TemplateView):

    template_name = 'admin/admin/password_change.html.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # each_context(self.request, context)

        context['title'] = _('Password change')

        return context


class PasswordChangeDoneView(TemplateView):

    pass


IndexView = admin_staff_member_required(IndexView.as_view())
LoginView = csrf_protect(never_cache(LoginView.as_view()))
LogoutView = admin_staff_member_required(LogoutView.as_view())
PasswordChangeView = admin_staff_member_required(PasswordChangeView.as_view(), cacheable=True)
PasswordChangeDoneView = admin_staff_member_required(PasswordChangeDoneView.as_view(), cacheable=True)
