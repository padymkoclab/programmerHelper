
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppRepliesConfig(AppConfig):
    name = "apps.app_replies"
    verbose_name = _("App Replies")

    def ready(self):
        pass
