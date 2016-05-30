
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class TestingConfig(AppConfig):
    name = 'apps.testing'
    verbose_name = _('Testing')
