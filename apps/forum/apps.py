
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'apps.forum'
    verbose_name = _('Forum')
