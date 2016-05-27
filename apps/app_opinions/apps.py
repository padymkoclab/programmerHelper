
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppOpinionsConfig(AppConfig):
    name = "apps.app_opinions"
    verbose_name = _("App Opinions")

    def ready(self):
        pass
