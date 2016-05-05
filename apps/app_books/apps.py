
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppBooksConfig(AppConfig):
    name = "apps.app_books"
    verbose_name = _("Books")
