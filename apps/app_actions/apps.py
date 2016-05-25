
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppActionsConfig(AppConfig):
    name = "apps.app_actions"
    verbose_name = _("Actions")

    def ready(self):
        from .signals import signal_deleted_course
        from .signals import signal_for_keeping_old_account
        from .signals import signal_created_updated_object
        from .signals import signal_deleted_object
        from .signals import signal_change_authorhip_of_course
        from .signals import signal_account_participated_in_poll
        from .signals import signal_account_removed_from_voters_in_poll
        from .signals import signal_creating_updating_of_account
        from .signals import signal_deleted_account
        from .signals import signal_change_useful_links_of_solutions_or_articles
