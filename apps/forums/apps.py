
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ForumsConfig(AppConfig):

    name = 'apps.forums'
    verbose_name = _('Forums')
    label = 'forums'
