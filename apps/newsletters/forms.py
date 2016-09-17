
from django import forms

from apps.core.widgets import CKEditorAdminWidget

from .models import Newsletter


class NewsletterAdminModelForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('user', 'content')
        widgets = {
            'content': CKEditorAdminWidget(attrs={
                'id': 'content_ckeditorwidget',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span10'
