
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class SolutionsConfig(AppConfig):
    name = 'apps.solutions'
    verbose_name = _('Solutions')
    label = 'solutions'
