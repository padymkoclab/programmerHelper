
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class VisitsConfig(AppConfig):
    name = "apps.visits"
    verbose_name = _("Visits")

    # def ready(self):
    #     from .signals import signal_change_slug
