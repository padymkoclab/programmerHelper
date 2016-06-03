
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings

from apps.tags.forms import clean_tags

from .models import Book


class BookForm(forms.ModelForm):
    """
    Form based on model Book
    """

    class Meta:
        model = Book
        fields = ['name']

    def clean_tags(self):
        super(BookForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags

    def clean_links(self):
        super(BookForm, self).clean()
        # validation restrict count weblinks where downloads
        links = self.cleaned_data.get('links', tuple())
        if len(links) > settings.MAX_COUNT_WEBLINKS_ON_OBJECT:
            self.add_error('links', _('Count links must be not more than {0}').format(
                settings.MAX_COUNT_WEBLINKS_ON_OBJECT
            ))
        return links
