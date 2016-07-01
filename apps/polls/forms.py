
from django import forms

from .models import Poll, Choice


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'slug', 'status')

    def __init__(self, *args, **kwargs):
        super(PollModelForm, self).__init__(*args, **kwargs)
        # make field slug as disabled
        self.fields['title'].widget.attrs = {
            'placeholder': 'Enter title of poll',
            'class': 'span',
        }
        self.fields['slug'].widget.attrs = {
            'class': 'span',
        }
        self.fields['slug'].disabled = True


class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('poll', 'text_choice')

    def __init__(self, *args, **kwargs):
        super(ChoiceModelForm, self).__init__(*args, **kwargs)
        self.fields['text_choice'].widget.attrs = {
            'placeholder': 'Enter text of choice',
            'class': 'span',
            'rows': 5,
        }
