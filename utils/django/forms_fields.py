
from django import forms

from .widgets import DurationSplitWidget


class DurationSplitField(forms.MultiValueField):

    widget = DurationSplitWidget

    def compress(self, data_list):
        raise NotImplementedError('Subclasses must implement this method.')
