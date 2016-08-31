
from django import forms

from suit.widgets import AutosizedTextarea

from .models import UtilityCategory, Utility


class UtilityCategoryAdminModelForm(forms.ModelForm):

    class Meta:
        model = UtilityCategory
        fields = ['name', 'slug', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['description'].widget = AutosizedTextarea(attrs={'class': 'span12'})


class UtilityAdminModelForm(forms.ModelForm):

    class Meta:
        model = Utility
        fields = ['name', 'category', 'description', 'web_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        # field with FK
        self.fields['category'].widget.widget.attrs['class'] = 'span11'

        self.fields['description'].widget = AutosizedTextarea(attrs={'class': 'span12'})

        self.fields['web_link'].widget.attrs['class'] = 'span12'
