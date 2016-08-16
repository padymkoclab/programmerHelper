
from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    ExportTemplateView, ExportPreviewDownloadView,
    ImportTemplateView, ImportResultTemplateView
)


app_name = 'export_import_models'


urlpatterns_for_export = [
    url(r'export/', include([
        url(r'(?P<contenttype_model_pk>\d+)/(?P<pks_separated_commas>[-,\w]*)/$', staff_member_required(ExportTemplateView.as_view()), {}, 'export'),
        url(r'download_preview/$', staff_member_required(ExportPreviewDownloadView.as_view()), {}, 'export_preview_download'),
    ])),
    url(r'import/', include([
        url(r'^$', staff_member_required(ImportTemplateView.as_view()), {}, 'import_model'),
        url(r'result/$', staff_member_required(ImportResultTemplateView.as_view()), {}, 'import_result'),
    ]))
]

urlpatterns_for_import = [

]

urlpatterns = urlpatterns_for_export + urlpatterns_for_import
