
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppScopesConfig(AppConfig):
    name = "apps.app_scopes"
    verbose_name = _("App Scopes")

    def ready(self):
        pass
