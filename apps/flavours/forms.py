
from django import forms

from .models import Flavour


class FlavourInlineAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span12'

    class Meta:
        model = Flavour
        fields = ['user', 'status']
