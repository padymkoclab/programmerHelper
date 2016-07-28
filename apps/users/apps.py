
# import uuid

# from django.core.signals import request_finished
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

from .signals import signal_post_migrate_model_levels_of_users


class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = _('Users')

    def ready(self):
        """ """

        post_migrate.connect(signal_post_migrate_model_levels_of_users, sender=self)
