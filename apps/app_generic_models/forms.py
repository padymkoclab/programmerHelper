
from collections import Counter

from django.utils.translation import ugettext_lazy as _
from django import forms


class ScopeGenericInlineFormSet(forms.BaseInlineFormSet):
    """
    Special inline form for relationship between TestQuestion and Varian models.
    """

    fk = 'content_object'

    def clean(self):
        """Validation what must unique numbers of lessons in formset."""
        super(ScopeGenericInlineFormSet, self).clean()
        raise Exception('Oooops')
        # all_numbers_of_lessons = list()
        # for form in self.forms:
        #     number = form.cleaned_data.get('number', None)
        #     all_numbers_of_lessons.append(number)
        # import pdb; pdb.set_trace()
        # t = list()
        # for key, value in Counter(all_numbers_of_lessons).items():
        #     if value > 1:
        #         t.append(key)
        # for form in self.forms:
        #     number = form.cleaned_data.get('number', None)
        #     if number in t:
        #         form.add_error('number', _('Please don`t repeat your number.'))
