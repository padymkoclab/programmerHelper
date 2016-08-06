
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Poll, Choice, Vote


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'slug', 'status')

    def __init__(self, *args, **kwargs):
        super(PollModelForm, self).__init__(*args, **kwargs)

        # add css class
        self.fields['title'].widget.attrs = {
            'placeholder': _('Enter a title of poll'),
            'autocomplete': 'off',
            # special css class for admin theme - django-suit
            # it allow made input on all width of container
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
            'placeholder': _('Enter text of choice'),
            'class': 'span11',
            'rows': 5,
        }

        # It is not worked
        # self.fields['poll'].widget.attrs['class'] = 'span12'
        self.fields['poll'].widget.attrs = {
            'class': 'span12',
            'id': 'span11',
            'name': 'span12',
            'style': 'span12',
            'multiple': 'multiple',
        }
