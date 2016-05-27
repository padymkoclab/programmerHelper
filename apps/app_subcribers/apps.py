
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppSubcribersConfig(AppConfig):
    name = "apps.app_subcribers"
    verbose_name = _("App Subcribers")

    def ready(self):
        pass
