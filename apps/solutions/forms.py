
from django import forms
from django.utils.translation import ugettext_lazy as _

# from suit_ckeditor.widgets import CKEditorWidget

from apps.tags.forms import clean_tags

from .models import Solution


class SolutionAdminModelForm(forms.ModelForm):
    """
    ModelForm for Solution.
    """

    class Meta:
        model = Solution
        fields = ('tags', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['problem'].widget.attrs['class'] = 'span12'
        self.fields['problem'].widget.attrs['placeholder'] = _('Enter problem')

        self.fields['slug'].disabled = True
        self.fields['slug'].widget.attrs['class'] = 'span12'

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        # self.fields['body'].widget = CKEditorWidget()

    def clean_tags(self):
        super().clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags
