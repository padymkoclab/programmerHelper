
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class PrivacyPolicyConfig(AppConfig):
    name = 'apps.privacy_policy'
    verbose_name = _('Privacy Policy')
