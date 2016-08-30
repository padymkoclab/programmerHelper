
from django import forms

from suit.widgets import AutosizedTextarea

from .models import Comment


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text_comment'].widget = AutosizedTextarea(attrs={'class': 'span12'})

        self.fields['user'].widget.widget.attrs['class'] = 'span11'
