
from django.conf.urls import url

from .views import IndexView, LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView


app_name = 'admin'


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
