
from django.conf.urls import url

from .views import IndexView, LoginView, LogoutView, PasswordChangeView

app_name = 'admin'


urlpatterns = [
    url(r'^$', IndexView.as_view(), {}, 'index'),
    url(r'^login/$', LoginView.as_view(), {}, 'login'),
    url(r'^logout/$', LogoutView.as_view(), {}, 'logout'),
    url(r'^password_change/$', PasswordChangeView.as_view(), {}, 'password_change'),
    # url(r'^password_change/done/$', IndexView.as_view(), {}, 'password_change_done'),
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
