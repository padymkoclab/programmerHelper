
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppSnippetsConfig(AppConfig):
    name = "apps.app_snippets"
    verbose_name = _("Snippets")
