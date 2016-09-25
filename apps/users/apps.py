
# import uuid

# from django.core.signals import request_finished
# from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

from .signals import (
    signal_post_migrate_model_levels_of_users,
    # auto_create_user_profile,
    # auto_delete_user_profile,
)


class UsersConfig(AppConfig):

    name = 'apps.users'
    verbose_name = _('Users')
    label = 'users'

    def ready(self):
        """ """

        # User = get_user_model()

        post_migrate.connect(signal_post_migrate_model_levels_of_users, sender=self)
