
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppPrivacyPolicyConfig(AppConfig):
    name = 'apps.app_privacy_policy'
    verbose_name = _('Privacy Policy')
