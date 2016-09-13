
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class QuestionsConfig(AppConfig):

    name = "apps.questions"
    verbose_name = _("Questions")
    label = 'questions'
