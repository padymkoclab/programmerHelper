
from django.utils.translation import ugettext_lazy as _

from django.forms import BaseInlineFormSet

from .models import Question, Variant


class QuestionInlineFormSet(BaseInlineFormSet):
    """
    Special inline form for relationship between Question and Varian models.
    """

    def get_unique_error_message(self, unique_check):

        if len(unique_check) == 1:
            return _("Please correct the duplicate data for %(field)s.") % {
                "field": unique_check[0],
            }
        else:
            return Question.MSG_UNIQUE_TOGETHER_TITLE_AND_SUIT


class VariantInlineFormSet(BaseInlineFormSet):
    """
    Special inline form for relationship between Question and Varian models.
    """

    def get_unique_error_message(self, unique_check):

        if len(unique_check) == 1:
            return _("Please correct the duplicate data for %(field)s.") % {
                "field": unique_check[0],
            }
        else:
            return Variant.MSG_UNIQUE_TOGETHER_QUESTION_AND_TEXT_VARIANT
