
from django import forms
from django.utils.translation import ugettext_lazy as _

from suit.widgets import AutosizedTextarea

# from .models import Poll, Choice


class PollAdminModelForm(forms.ModelForm):

    class Meta:
        widgets = {
            'status': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = _('Enter a title of poll')
        self.fields['title'].widget.attrs['autocomplete'] = 'off'
        self.fields['title'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True


class ChoiceAdminInlineModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text_choice'].widget = AutosizedTextarea(attrs={
            'placeholder': _('Enter text of a choice'),
            'class': 'span11',
        })
