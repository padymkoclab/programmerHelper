
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppAccountsConfig(AppConfig):
    name = 'apps.app_accounts'
    verbose_name = _('Accounts')
