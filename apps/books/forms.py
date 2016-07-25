
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings

from apps.tags.forms import clean_tags

from .models import Book, Writter


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name']

    def clean_tags(self):
        super(BookForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags


class WritterForm(forms.ModelForm):
    class Meta:
        model = Writter
        fields = ('name',)

    def clean(self):
        super(WritterForm, self).clean()
