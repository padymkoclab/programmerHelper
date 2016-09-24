
from django.utils.translation import ugettext_lazy as _
from django import forms

# from suit_ckeditor.widgets import CKEditorWidget

# from apps.core.widgets import CKEditorAdminWidget


class PartitionInlineAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')
        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['content'].widget.attrs['placeholder'] = _('Enter content')
        self.fields['content'].widget.attrs['class'] = 'span12'
