
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppTestingConfig(AppConfig):
    name = 'apps.app_testing'
    verbose_name = _('Testing')
