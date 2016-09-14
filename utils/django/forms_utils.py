
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django import forms


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """ """

    def render(self):
        """ """

        return mark_safe(''.join(['{}'.format(w) for w in self]))


class HorizontalRadioSelect(forms.RadioSelect):

    renderer = HorizontalRadioRenderer


class BooleanRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = [(True, _('Yes')), (False, _('No'))]
