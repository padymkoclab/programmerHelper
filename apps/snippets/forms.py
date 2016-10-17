
from django import forms

# from suit.widgets import AutosizedTextarea
# from suit_ckeditor.widgets import CKEditorWidget

from apps.tags.forms import clean_tags


class SnippetAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SnippetAdminModelForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

    class Meta:
        widgets = {
            # 'description': AutosizedTextarea(attrs={'class': 'span11'}),
            # 'code': CKEditorWidget(editor_options={'startupFocus': True}),
        }

    def clean_tags(self):
        super(SnippetAdminModelForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags
