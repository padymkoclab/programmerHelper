
import collections

from django.utils.translation import ugettext_lazy as _
from django.forms import BaseInlineFormSet

from .models import Choice
from .constants import MIN_COUNT_CHOICES_IN_POLL


class ChoiceInlineFormSet(BaseInlineFormSet):
    """
    Formset for choices. Used for prevent input choices with same text.
    """

    def clean(self):

        # make additional validations if form is valid
        if self.is_valid():

            # get all text input,
            all_texts = list()
            for form in self.forms:
                text_choice = form.cleaned_data.get('text_choice', None)
                if text_choice is not None:
                    all_texts.append(text_choice)

            # count all a texts
            counter_texts = collections.Counter(all_texts)

            # filter only dublicated texts
            # made a iterator as a tuple, because any iterator have a habit use up for once
            duplicated_text = tuple(
                text for text, count_encounters in counter_texts.items()
                if count_encounters > 1
            )

            # again make iteration on all forms
            # and add error message, if need, to the forms with dublicate texts
            for form in self.forms:
                if form.cleaned_data.get('text_choice', None) in duplicated_text:
                    form.add_error('text_choice', Choice.UNIQUE_ERROR_MESSAGE_FOR_TEXT_CHOICE_AND_POLL)

        # if is forms for delete
        # deterninate count choices in poll, after delete any count choices
        # if after deleting the choices this poll will be have a count choices less than min count choices in poll,
        # than add error to all formset
        if self.deleted_forms:
            count_deleted_forms = len(self.deleted_forms)
            count_total_forms = len(self.forms)
            if count_total_forms - count_deleted_forms < MIN_COUNT_CHOICES_IN_POLL:
                self._non_form_errors.append(
                    _('You try delete choices more than must be minimal number of choices in an each poll.')
                )
