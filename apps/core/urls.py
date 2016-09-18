
from django.conf import settings
from django.conf.urls.static import static
# from django.views.decorators.cache import cache_page
from django.conf.urls import url, include
from django.views.i18n import javascript_catalog
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django_js_reverse.views import urls_js

from .admin import AdminSite
from .views import IndexView, PlaceholderView

js_info_dict = {
    'packages': ('your.app.package',),
}

urlpatterns = [

    # django
    url(r'^admin/export_import/', include('apps.export_import_models.urls')),
    url(r'^admin/', AdminSite.urls),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, 'javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # project
    url(r'^$', IndexView.as_view(), {}, 'index'),
    url(r'^image/(?P<height>\d+)x(?P<width>\d+)/$', PlaceholderView.as_view(), {}, 'placeholder'),
    # url(r'^django_js_reverse/$', cache_page(3600)(urls_js), name='django_js_reverse'),

    # apps
    url(r'^users/', include('apps.users.urls')),
    url(r'^activity/', include('apps.activity.urls')),
    url(r'^articles/', include('apps.articles.urls')),
    url(r'^library/', include('apps.library.urls')),
    # url(r'^courses/', include('apps.courses.urls')), # temporary is disabled
    url(r'^forum/', include('apps.forums.urls')),
    url(r'^notifications/', include('apps.notifications.urls')),
    url(r'^news/', include('apps.newsletters.urls')),
    url(r'^polls/', include('apps.polls.urls')),
    url(r'^questions/', include('apps.questions.urls')),
    url(r'^snippets/', include('apps.snippets.urls')),
    url(r'^solutions/', include('apps.solutions.urls')),
    url(r'^tags/', include('apps.tags.urls')),
    url(r'^testing/', include('apps.testing.urls')),
    url(r'^utilities/', include('apps.utilities.urls')),
]

# Additional urls for static (only for development local)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
