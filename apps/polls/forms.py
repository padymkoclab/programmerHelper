
from django import forms

from .models import Poll, Choice, VoteInPoll


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'slug', 'status')

    def __init__(self, *args, **kwargs):
        super(PollModelForm, self).__init__(*args, **kwargs)

        # add css class
        self.fields['title'].widget.attrs = {
            'placeholder': 'Enter title of poll',
            'class': 'span12',
        }
        self.fields['slug'].widget.attrs = {
            'class': 'span12',
        }
        self.fields['status'].widget.attrs = {
            'class': 'span12',
        }

        # make field slug as disabled
        self.fields['slug'].disabled = True


class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('poll', 'text_choice')

    def __init__(self, *args, **kwargs):
        super(ChoiceModelForm, self).__init__(*args, **kwargs)
        self.fields['text_choice'].widget.attrs = {
            'placeholder': 'Enter text of choice',
            'class': 'span12',
            'rows': 5,
        }

        # It is not worked
        self.fields['poll'].widget.attrs['class'] = 'span11'


class VoteInPollModelForm(forms.ModelForm):
    class Meta:
        model = VoteInPoll
        fields = ('account', 'poll', 'choice')

    def __init__(self, *args, **kwargs):
        super(VoteInPollModelForm, self).__init__(*args, **kwargs)

        # It is not worked
        self.fields['account'].widget.attrs['class'] = 'span1'
        self.fields['poll'].widget.attrs['class'] = 'span1'
        self.fields['choice'].widget.attrs['class'] = 'span1'
