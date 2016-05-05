
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppTagsConfig(AppConfig):
    name = 'apps.app_tags'
    verbose_name = _('Tags')
