
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class CountriesConfig(AppConfig):
    name = "apps.countries"
    verbose_name = _("Countries")

    def ready(self):
        pass
