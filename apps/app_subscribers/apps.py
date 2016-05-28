
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppSubscribersConfig(AppConfig):
    name = "apps.app_subscribers"
    verbose_name = _("App Subscribers")

    def ready(self):
        pass
