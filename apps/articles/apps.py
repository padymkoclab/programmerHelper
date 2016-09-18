
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ArticlesConfig(AppConfig):

    name = 'apps.articles'
    verbose_name = _('Articles')
    label = 'articles'
