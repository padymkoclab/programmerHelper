
from django.utils.translation import ugettext_lazy as _
from django import forms


class UploadSerializedFileForm(forms.Form):

    file = forms.FileField(
        label=_('Select a file'),
        # help_text=_('Format of file must be JSON, XML or YAML'),
        widget=forms.FileInput,
    )
