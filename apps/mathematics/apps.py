
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppMathematicsConfig(AppConfig):
    name = "apps.app_mathematics"
    verbose_name = _("App Mathematics")

    def ready(self):
        pass
