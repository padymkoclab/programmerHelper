
from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    ExportTemplateView, ExportPreviewDownloadView, ExportRedirectView,
    ImportTemplateView
)


app_name = 'export_import_models'


urlpatterns_for_export = [
    url(r'export_model/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<pks_separated_commas>[-,\w]*)', staff_member_required(ExportRedirectView.as_view()), {}, 'export_model'),
    url(r'export/', include([
        url(r'(?P<content_type_model_pk>\d+)/(?P<pks_separated_commas>[-,\w]*)/$', staff_member_required(ExportTemplateView.as_view()), {}, 'export'),
        url(r'download_preview/', staff_member_required(ExportPreviewDownloadView.as_view()), {}, 'export_preview_download'),
    ])),
    url(r'import_model/', staff_member_required(ImportTemplateView.as_view()), {}, 'import_model'),
]

urlpatterns_for_import = [

]

urlpatterns = urlpatterns_for_export + urlpatterns_for_import
