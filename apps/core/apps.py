
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "apps.core"
    verbose_name = _("Core")

    def ready(self):

        from .signals import added_update_object, deleted_object
