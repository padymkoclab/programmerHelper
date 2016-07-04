
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ExportImportModelsConfig(AppConfig):
    name = "apps.export_import_models"
    verbose_name = _("Export Import Models")

    def ready(self):
        pass
