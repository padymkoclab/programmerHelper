
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import forms

from utils.django.formsets_utils import find_dublication_on_formset


class FlavourFormSet(forms.BaseGenericInlineFormSet):

    def clean(self):

        super().clean()

        find_dublication_on_formset(
            self,
            'user',
            _('User may has only one flavour about object'),
            _('Repeated user'),
        )
