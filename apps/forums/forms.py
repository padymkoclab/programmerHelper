
from django import forms
from django.utils.translation import ugettext_lazy as _

from utils.django.widgets import AdminImageThumbnail

from .models import Section


class SectionAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['position'].widget.attrs['class'] = 'span2'

    class Meta:
        model = Section
        fields = ('name', 'groups', 'position', 'image')
        widgets = {
            'image': AdminImageThumbnail(),
        }
