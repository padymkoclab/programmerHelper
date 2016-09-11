
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class SnippetsConfig(AppConfig):
    name = "apps.snippets"
    verbose_name = _("Snippets")
    label = 'snippets'
