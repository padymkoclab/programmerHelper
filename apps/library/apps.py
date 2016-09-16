
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class LibraryConfig(AppConfig):

    name = "apps.library"
    verbose_name = _("Library")
    label = 'library'
