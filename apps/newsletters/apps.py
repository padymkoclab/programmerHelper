
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class NewslettersConfig(AppConfig):

    name = "apps.newsletters"
    verbose_name = _("Newsletters")
    label = 'newsletters'
