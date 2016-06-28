
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class MarksConfig(AppConfig):
    name = "apps.marks"
    verbose_name = _("Marks")

    def ready(self):
        pass
