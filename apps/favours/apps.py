
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class FavoursConfig(AppConfig):
    name = "apps.favours"
    verbose_name = _("App Favours")

    def ready(self):
        pass
