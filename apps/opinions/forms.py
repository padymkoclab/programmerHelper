
from django import forms

from .models import Opinion


class OpinionInlineAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span12'

    class Meta:
        model = Opinion
        fields = ['user', 'is_useful']
