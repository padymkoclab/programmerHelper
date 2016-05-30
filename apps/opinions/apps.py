
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class OpinionsConfig(AppConfig):
    name = "apps.opinions"
    verbose_name = _("App Opinions")

    def ready(self):
        pass
