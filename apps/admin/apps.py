
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AdminConfig(AppConfig):

    name = 'apps.admin'
    verbose_name = _('Admin')
    label = 'admin'
