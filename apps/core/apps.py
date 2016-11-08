
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class CoreConfig(AppConfig):

    name = "apps.core"
    verbose_name = _("Core")
    app_label = 'core'

    def ready(self):

        from .signals import (
            post_added_updated_object,
            pre_deleted_object,
            changed_group,
            login_user,
            logout_user,
            failed_login_user,
        )
