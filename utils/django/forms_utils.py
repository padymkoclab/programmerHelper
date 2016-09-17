
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django import forms


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """ """

    def render(self):
        """ """

        return mark_safe(''.join(['{}'.format(w) for w in self]))
