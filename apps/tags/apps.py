
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class TagsConfig(AppConfig):
    name = 'apps.tags'
    verbose_name = _('Tags')
