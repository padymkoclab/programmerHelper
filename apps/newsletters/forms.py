
from django import forms

from apps.core.widgets import CKEditorAdminWidget


class NewsletterAdminModelForm(forms.ModelForm):

    class Meta:
        widgets = {
            'content': CKEditorAdminWidget(attrs={
                'id': 'content_ckeditorwidget',
            }),
        }
