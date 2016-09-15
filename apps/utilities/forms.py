
from django import forms
from django.utils.translation import ugettext_lazy as _

from suit.widgets import AutosizedTextarea

from .models import Category, Utility


class CategoryAdminModelForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['description'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter description'),
        })


class UtilityAdminModelForm(forms.ModelForm):

    class Meta:
        model = Utility
        fields = ['name', 'category', 'description', 'web_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['category'].widget.widget.attrs['class'] = 'span11'

        self.fields['description'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter description'),
        })

        self.fields['web_link'].widget.attrs['class'] = 'span12'
        self.fields['web_link'].widget.attrs['placeholder'] = _('Enter link in web')
