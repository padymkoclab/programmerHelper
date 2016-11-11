
from django.utils.translation import ugettext_lazy as _
from django import apps


class AppConfig(apps.AppConfig):

    name = 'app'
    verbose_name = _('App')
    label = 'app'
