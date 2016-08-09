
from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    ExportTemplateView, ExportPreviewDownloadView, ExportCSV, ExportExcel, ExportRedirectView
)


app_name = 'export_import_models'


urlpatterns_for_export = [
    url(
        r'export_model/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<pks_separated_commas>[-,\w]*)',
        staff_member_required(ExportRedirectView.as_view()),
        {},
        'export_model'
    ),
    url(r'export/', include([
        url(
            r'(?P<ct_model_pk>\d+)/(?P<pks_separated_commas>[-,\w]*)/$',
            staff_member_required(ExportTemplateView.as_view()),
            {},
            'export'
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
    ]))
]

urlpatterns_for_import = [

]

urlpatterns = urlpatterns_for_export + urlpatterns_for_import
