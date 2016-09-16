
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django import forms


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """ """

    def render(self):
        """ """

        return mark_safe(''.join(['{}'.format(w) for w in self]))


class HorizontalRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        css_style = 'style="display: inline-block; margin-right: 10px;"'

        self.renderer.inner_html = '<li ' + css_style + '>{choice_value}{sub_widgets}</li>'


class BooleanRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = [(True, _('Yes')), (False, _('No'))]
