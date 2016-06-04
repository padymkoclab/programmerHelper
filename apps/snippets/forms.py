
from django import forms

from apps.tags.forms import clean_tags

from .models import Snippet


class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ('title', )

    def clean_tags(self):
        super(SnippetForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags
