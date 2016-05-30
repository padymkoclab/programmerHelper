
from django.conf.urls import url, include
from django.views.i18n import javascript_catalog

from .admin import ProgrammerHelper_AdminSite
from .views import IndexView

js_info_dict = {
    'packages': ('your.app.package',),
}

urlpatterns = [
    # django
    url(r'^admin/', ProgrammerHelper_AdminSite.urls),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # main
    url(r'^$', IndexView.as_view(), {}, 'index'),
    # url(r'^$', IndexView.as_view(), {}, 'index'),
    # apps
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^actions/', include('apps.actions.urls')),
    url(r'^articles/', include('apps.articles.urls')),
    url(r'^books/', include('apps.books.urls')),
    url(r'^courses/', include('apps.courses.urls')),
    url(r'^forum/', include('apps.forum.urls')),
    url(r'^inboxes/', include('apps.inboxes.urls')),
    url(r'^news/', include('apps.newsletters.urls')),
    url(r'^polls/', include('apps.polls.urls')),
    url(r'^questions/', include('apps.questions.urls')),
    url(r'^snippets/', include('apps.snippets.urls')),
    url(r'^solutions/', include('apps.solutions.urls')),
    url(r'^tags/', include('apps.tags.urls')),
    url(r'^testing/', include('apps.testing.urls')),
    url(r'^utilities/', include('apps.utilities.urls')),
]
