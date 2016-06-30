
import collections

from django.forms import BaseInlineFormSet

from .models import Choice


class ChoiceInlineFormSet(BaseInlineFormSet):
    """
    Formset for choices. Used for prevent input choices with same text.
    """

    def clean(self):

        # make additional validations if form is valid
        if self.is_valid():

            # count all a texts
            counter_texts = collections.Counter(form.cleaned_data['text_choice'] for form in self.forms)

            # filter only dublicated texts
            # made a iterator as a tuple, because any iterator have a habit use up for once
            duplicated_text = tuple(
                text for text, count_encounters in counter_texts.items()
                if count_encounters > 1
            )

            # again make iteration on all forms
            # and add error message, if need, to the forms with dublicate texts
            for form in self.forms:
                if form.cleaned_data['text_choice'] in duplicated_text:
                    form.add_error('text_choice', Choice.UNIQUE_ERROR_MESSAGE_FOR_TEXT_CHOICE_AND_POLL)
