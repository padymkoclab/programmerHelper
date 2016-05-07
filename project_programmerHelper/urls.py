
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
    url(r'^$', IndexView, {}, 'index'),
    # url(r'^$', IndexView.as_view(), {}, 'index'),
    # apps
    url(r'^accounts/', include('apps.app_accounts.urls')),
    url(r'^books/', include('apps.app_books.urls')),
    url(r'^articles/', include('apps.app_articles.urls')),
    url(r'^forum/', include('apps.app_forum.urls')),
    url(r'^solutions/', include('apps.app_solutions.urls')),
    url(r'^tags/', include('apps.app_tags.urls')),
    url(r'^snippets/', include('apps.app_snippets.urls')),
    url(r'^news/', include('apps.app_newsletters.urls')),
    url(r'^polls/', include('apps.app_polls.urls')),
    url(r'^programming_tester/', include('apps.app_programming_tester.urls')),
    url(r'^programming_utilities/', include('apps.app_programming_utilities.urls')),
]
