
from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    ExportTemplateView, ExportPreviewDownloadView, ExportCSV, ExportExcel, ExportPDF
)


app_name = 'export_import_models'


urlpatterns_for_export = [
    url(r'export/', include([
        url(
            r'(?P<ct_model_pk>\d+)/(?P<objects_pks>[-,\w]+)/$',
            staff_member_required(ExportTemplateView.as_view()),
            {},
            'admin_export'
        ),
        url(
            r'/'.join([
                '(?P<mode>(preview|download))',
                '(?P<format>(json|yaml|xml))',
                '(?P<ct_model_pk>[-\w]+)',
                '(?P<fields>[_,\w]+)',
                '(?P<objects_pks>[-,\w]+)',
                '$',
            ]),
            staff_member_required(ExportPreviewDownloadView.as_view()),
            {},
            'admin_export_preview'
        ),
        url(
            r'/'.join([
                'csv',
                '(?P<ct_model_pk>[-\w]+)',
                '(?P<fields>[_,\w]+)',
                '(?P<objects_pks>[-,\w]+)',
                '$',
            ]),
            staff_member_required(ExportCSV.as_view()),
            {},
            'admin_export_csv',
        ),
        url(
            r'/'.join([
                'excel',
                '(?P<ct_model_pk>[-\w]+)',
                '(?P<fields>[_,\w]+)',
                '(?P<objects_pks>[-,\w]+)',
                '$',
            ]),
            staff_member_required(ExportExcel.as_view()),
            {},
            'admin_export_excel',
        ),
        url(
            r'pdf/',
            staff_member_required(ExportPDF.as_view()),
            {},
            'admin_export_pdf',
        ),
    ]))
]

urlpatterns_for_import = [

]

urlpatterns = urlpatterns_for_export + urlpatterns_for_import
