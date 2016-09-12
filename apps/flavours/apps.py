
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class FlavoursConfig(AppConfig):
    name = "apps.flavours"
    verbose_name = _("Flavours")

    def ready(self):
        pass
