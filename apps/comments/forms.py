
from django.utils.translation import ugettext_lazy as _
from django import forms

from suit.widgets import AutosizedTextarea

from .models import Comment


class CommentInlineAdminModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text_comment', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text_comment'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter text of comment'),
        })

        self.fields['user'].widget.widget.attrs['class'] = 'span11'
