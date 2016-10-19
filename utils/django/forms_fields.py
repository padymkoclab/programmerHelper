
from django import forms

from .widgets import DurationSplitWidget, TextInputFixed


class DurationSplitField(forms.MultiValueField):

    widget = DurationSplitWidget

    def compress(self, data_list):
        raise NotImplementedError('Subclasses must implement this method.')


class CharFieldFixed(forms.CharField):

    def __init__(self, *args, **kwargs):

        modelfield = kwargs.pop('modelfield')
        super(CharFieldFixed, self).__init__(*args, **kwargs)

        self.widget = TextInputFixed()
        self.widget.modelfield = modelfield
