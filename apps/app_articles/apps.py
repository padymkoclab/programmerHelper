
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AppArticlesConfig(AppConfig):
    name = 'apps.app_articles'
    verbose_name = _('Articles')
