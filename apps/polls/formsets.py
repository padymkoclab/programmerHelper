
import collections

from django.utils.translation import ugettext_lazy as _
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
        if self.deleted_forms:
            # import ipdb; ipdb.set_trace()
            for form in self.deleted_forms:
                form.add_error('__all__', _('You don`t have delete choices when to try add new votes.'))
            # self.can_delete = False
