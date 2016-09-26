
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .signals import (
    create_default_badges,
)


class BadgesConfig(AppConfig):

    name = 'apps.badges'
    verbose_name = _('Badges')
    label = 'badges'

    def ready(self):

        post_migrate.connect(create_default_badges, sender=self)
