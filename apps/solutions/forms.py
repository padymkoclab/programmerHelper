
from django import forms

from suit_ckeditor.widgets import CKEditorWidget

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
        super(SolutionAdminModelForm, self).__init__(*args, **kwargs)

        self.fields['problem'].widget.attrs['class'] = 'span12'

        self.fields['slug'].disabled = True
        self.fields['slug'].widget.attrs['class'] = 'span12'

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        self.fields['body'].widget = CKEditorWidget()

    def clean_tags(self):
        super(SolutionAdminModelForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags
