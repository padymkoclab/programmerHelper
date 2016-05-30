
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class RepliesConfig(AppConfig):
    name = "apps.replies"
    verbose_name = _("App Replies")

    def ready(self):
        pass
