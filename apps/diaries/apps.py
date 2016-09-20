
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class DiaryConfig(AppConfig):

    name = 'apps.diaries'
    verbose_name = _('Diaries')
    label = 'diaries'
