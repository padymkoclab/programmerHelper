
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = "apps.comments"
    verbose_name = _("Comments")

    def ready(self):
        pass
