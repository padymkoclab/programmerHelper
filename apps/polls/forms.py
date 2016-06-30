
from django import forms

from .models import Poll, Choice


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'slug', 'status')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title of poll',
                'style': 'width: 98%',
            }),
            'slug': forms.TextInput(attrs={
                'style': 'width: 98%',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PollModelForm, self).__init__(*args, **kwargs)
        # make field slug as disabled
        self.fields['slug'].disabled = True


class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('poll', 'text_choice')
        widgets = {
            'text_choice': forms.Textarea(attrs={
                'placeholder': 'Enter text of choice',
                'style': 'width: 98%',
                'rows': 5,
            })
        }
