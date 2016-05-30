
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ScopesConfig(AppConfig):
    name = "apps.scopes"
    verbose_name = _("App Scopes")

    def ready(self):
        pass
