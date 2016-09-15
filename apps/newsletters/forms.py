
import json

from django import forms
from django.utils.safestring import mark_safe

from suit_ckeditor.widgets import CKEditorWidget

from .models import Newsletter


# Problem CREditor and field 'content'
# see https://github.com/darklow/django-suit/issues/182
class CKEditorWidgetForFieldContent(CKEditorWidget):
    def render(self, name, value, attrs=None):
        output = super(CKEditorWidget, self).render(name, value, attrs)
        output += mark_safe(
            '<script type="text/javascript">CKEDITOR.replace("%s", %s);</script>'
            % (self.attrs['id'], json.dumps(self.editor_options)))
        return output


class NewsletterAdminModelForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('user', 'content')
        widgets = {
            'content': CKEditorWidgetForFieldContent(attrs={
                'id': 'content_ckeditorwidget',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span10'
