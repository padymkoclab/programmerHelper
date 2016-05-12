
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import *


class BookForm(forms.ModelForm):
    """
    Form based on model Book
    """

    class Meta:
        model = Book
        fields = ['name']

    def clean(self):
        # validation restrict count tags
        tags = self.cleaned_data.get('tags', tuple())
        if not settings.MIN_COUNT_TAGS_ON_OBJECT <= len(tags) <= settings.MAX_COUNT_TAGS_ON_OBJECT:
            self.add_error('tags', _('Count tags must be from {0} to {1}').format(
                settings.MIN_COUNT_TAGS_ON_OBJECT,
                settings.MAX_COUNT_TAGS_ON_OBJECT,
                )
            )
        # validation restrict count weblinks where downloads
        links = self.cleaned_data.get('links', tuple())
        if len(links) > settings.MAX_COUNT_WEBLINKS_ON_OBJECT:
            self.add_error('links', _('Count links must be not more than {0}'.format(
                settings.MAX_COUNT_WEBLINKS_ON_OBJECT
                )
            ))
