
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppPollsConfig(AppConfig):
    name = "apps.app_polls"
    verbose_name = _("Polls")
