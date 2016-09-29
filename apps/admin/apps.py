
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

from django.contrib.admin.checks import check_admin_app, check_dependencies
from django.core import checks


class AdminConfig(AppConfig):

    name = 'apps.admin'
    verbose_name = _('Admin')
    label = 'admin'

    def ready(self):
        checks.register(check_dependencies, checks.Tags.admin)
        checks.register(check_admin_app, checks.Tags.admin)
