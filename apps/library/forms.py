
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django import forms

# from suit.widgets import AutosizedTextarea

from utils.django.widgets import AdminImageThumbnail

from apps.tags.forms import clean_tags

from .models import Book, Writer, Publisher


NOW_YEAR = timezone.now().year


class BookAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['slug'].disabled = True
        self.fields['slug'].widget.attrs['class'] = 'span12'

        # self.fields['description'].widget = AutosizedTextarea(attrs={'rows': 3, 'class': 'span12'})

        self.fields['image'].widget = AdminImageThumbnail()

        self.fields['count_pages'].widget.attrs['class'] = 'span12'
        self.fields['count_pages'].widget.input_type = 'number'
        self.fields['count_pages'].widget.attrs['min'] = 1

        self.fields['year_published'].widget.attrs['class'] = 'span12'
        self.fields['year_published'].widget.input_type = 'number'
        self.fields['year_published'].widget.attrs['min'] = Book.MIN_YEAR_PUBLISHED
        self.fields['year_published'].widget.attrs['max'] = NOW_YEAR

        self.fields['isbn'].widget.attrs['class'] = 'span10'

        self.fields['publisher'].widget.attrs['class'] = 'span12'

    class Meta:
        model = Book
        fields = ['name']

    def clean_tags(self):
        super().clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags


class WriterAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        # self.fields['about'].widget = AutosizedTextarea(attrs={'rows': 3, 'class': 'span12'})

        self.fields['trends'].widget.attrs['class'] = 'span12'

        self.fields['birth_year'].widget.input_type = 'number'
        self.fields['birth_year'].widget.attrs['min'] = Writer.MIN_BIRTH_YEAR
        self.fields['birth_year'].widget.attrs['max'] = Writer.MAX_BIRTH_YEAR

        self.fields['death_year'].widget.input_type = 'number'
        self.fields['death_year'].widget.attrs['min'] = Writer.MIN_DEATH_YEAR
        self.fields['death_year'].widget.attrs['max'] = NOW_YEAR

    class Meta:
        model = Writer
        fields = ('name',)

    def clean(self):
        super().clean()


class PublisherAdminModelForm(forms.ModelForm):

    class Meta:
        model = Publisher
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['country_origin'].widget.attrs['class'] = 'span12'

        self.fields['headquarters'].widget.attrs['class'] = 'span12'
        self.fields['headquarters'].widget.attrs['placeholder'] = _('Enter headquarters of company')

        self.fields['founded_year'].widget.input_type = 'number'
        self.fields['founded_year'].widget.attrs['class'] = 'span2'
        self.fields['founded_year'].widget.attrs['min'] = Publisher.MIN_FOUNDED_YEAR
        self.fields['founded_year'].widget.attrs['max'] = NOW_YEAR
        self.fields['founded_year'].widget.attrs['placeholder'] = _('Enter founded year')

        self.fields['website'].widget.attrs['class'] = 'span12'
        self.fields['website'].widget.attrs['placeholder'] = _('Enter name')
