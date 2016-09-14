
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class PollsConfig(AppConfig):

    name = "apps.polls"
    verbose_name = _("Polls")
    label = 'polls'
