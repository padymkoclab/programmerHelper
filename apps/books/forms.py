
from django.utils.translation import ugettext_lazy as _
from django import forms

from suit.widgets import AutosizedTextarea

from utils.django.widgets import AdminImageThumbnail

from apps.tags.forms import clean_tags

from .models import Book, Writer, Publisher


class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        # Full width
        self.fields['name'].widget.attrs['class'] = 'span12'

        # Full width and disabled
        self.fields['slug'].disabled = True
        self.fields['slug'].widget.attrs['class'] = 'span12'

        # Full width and auto resized (with jQuery script)
        # Worked only with the Django-Suit
        self.fields['description'].widget = AutosizedTextarea(attrs={'rows': 3, 'class': 'span12'})

        # Image with thumbnail
        self.fields['picture'].widget = AdminImageThumbnail()

        # Full width and FileInput
        self.fields['count_pages'].widget.attrs['class'] = 'span12'
        self.fields['count_pages'].widget.input_type = 'number'
        self.fields['count_pages'].widget.attrs['min'] = 1

        # Full width and FileInput
        self.fields['year_published'].widget.attrs['class'] = 'span12'
        self.fields['year_published'].widget.input_type = 'number'
        self.fields['year_published'].widget.attrs['min'] = Book.MIN_YEAR_PUBLISHED
        self.fields['year_published'].widget.attrs['max'] = Book.MAX_YEAR_PUBLISHED

        # Almost full width (considering help_text)
        self.fields['isbn'].widget.attrs['class'] = 'span10'

        # Full width
        self.fields['publishers'].widget.attrs['class'] = 'span12'

    class Meta:
        model = Book
        fields = ['name']

    def clean_tags(self):
        super(BookForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags


class WriterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WriterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['about'].widget = AutosizedTextarea(attrs={'rows': 3, 'class': 'span12'})

        self.fields['trends'].widget.attrs['class'] = 'span12'

        self.fields['birth_year'].widget.input_type = 'number'
        self.fields['birth_year'].widget.attrs['min'] = Writer.MIN_BIRTH_YEAR
        self.fields['birth_year'].widget.attrs['max'] = Writer.MAX_BIRTH_YEAR

        self.fields['death_year'].widget.input_type = 'number'
        self.fields['death_year'].widget.attrs['min'] = Writer.MIN_DEATH_YEAR
        self.fields['death_year'].widget.attrs['max'] = Writer.MAX_DEATH_YEAR

    class Meta:
        model = Writer
        fields = ('name',)

    def clean(self):
        super(WriterForm, self).clean()


class PublisherForm(forms.ModelForm):

    class Meta:
        model = Publisher
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(PublisherForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['country_origin'].widget.attrs['class'] = 'span12'

        self.fields['headquarters'].widget.attrs['class'] = 'span12'

        self.fields['founded_year'].widget.input_type = 'number'
        self.fields['founded_year'].widget.attrs['min'] = Publisher.MIN_FOUNDED_YEAR
        self.fields['founded_year'].widget.attrs['max'] = Publisher.MAX_FOUNDED_YEAR

        self.fields['website'].widget.attrs['class'] = 'span12'
