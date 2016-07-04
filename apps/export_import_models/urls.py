
from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required

from .views import ExportTemplateView, ExportPreviewView, ExportCSV


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
                '$']),
            staff_member_required(ExportPreviewView.as_view()),
            {},
            'admin_export_preview'
        ),
        url(
            r'csv/',
            staff_member_required(ExportCSV.as_view()),
            {},
            'admin_export_csv',
        ),
        url(
            r'excel/',
            staff_member_required(ExportCSV.as_view()),
            {},
            'admin_export_excel',
        )
    ]))
]

urlpatterns_for_import = [

]

urlpatterns = urlpatterns_for_export + urlpatterns_for_import
