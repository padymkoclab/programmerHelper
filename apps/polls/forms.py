
# from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Poll, Choice


class PollModelForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ('title', 'slug', 'status')

    def __init__(self, *args, **kwargs):
        super(PollModelForm, self).__init__(*args, **kwargs)

        # add css class
        # special css class for admin theme - django-suit
        # it allow made input on all width of container

        self.fields['title'].widget.attrs['placeholder'] = _('Enter a title of poll')
        self.fields['title'].widget.attrs['autocomplete'] = 'off'
        self.fields['title'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['status'].widget.attrs['class'] = 'span12'

        # make field slug as disabled
        self.fields['slug'].disabled = True


class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('poll', 'text_choice')

    def __init__(self, *args, **kwargs):
        super(ChoiceModelForm, self).__init__(*args, **kwargs)
        self.fields['text_choice'].widget.attrs = {
            'placeholder': _('Enter text of a choice'),
            'class': 'span11',
            'rows': 5,
        }

        # for FK field in ModelForm django create sppecial RelatedFieldWidgetWrapper
        # for it assignmention css class must next, but it is worked only in admin
        # self.fields['poll'].widget.widget.attrs['class'] = 'span11'
