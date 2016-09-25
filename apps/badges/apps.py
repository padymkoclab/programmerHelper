
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class BadgesConfig(AppConfig):

    name = 'apps.badges'
    verbose_name = _('Badges')
    label = 'badges'
