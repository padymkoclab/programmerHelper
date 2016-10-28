
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

from .signals import create_tags_if_yet_not


class TagsConfig(AppConfig):

    name = 'apps.tags'
    verbose_name = _('Tags')
    label = 'tags'

    def ready(self):

        post_migrate.connect(create_tags_if_yet_not, self)
