
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppFavoursConfig(AppConfig):
    name = "apps.app_favours"
    verbose_name = _("App Favours")

    def ready(self):
        pass
