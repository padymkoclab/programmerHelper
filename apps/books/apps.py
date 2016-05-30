
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = "apps.books"
    verbose_name = _("Books")
