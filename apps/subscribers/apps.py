
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class SubscribersConfig(AppConfig):
    name = "apps.subscribers"
    verbose_name = _("App Subscribers")

    def ready(self):
        pass
