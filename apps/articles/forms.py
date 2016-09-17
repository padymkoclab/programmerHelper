
from django.utils.translation import ugettext_lazy as _
from django import forms

from suit.widgets import AutosizedTextarea
from apps.core.widgets import CKEditorAdminWidget

from utils.django.widgets import AdminImageThumbnail

from apps.tags.forms import clean_tags

from .models import Article, Subsection


class ArticleAdminModelForm(forms.ModelForm):
    """

    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'
        self.fields['title'].widget.attrs['placeholder'] = _('Enter title')

        self.fields['slug'].disabled = True
        self.fields['slug'].widget.attrs['class'] = 'span12'

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        self.fields['quotation'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter quotation'),
        })

    class Meta:
        model = Article
        fields = ('tags', 'links', 'slug')
        widgets = {
            'status': forms.RadioSelect(),
            'image': AdminImageThumbnail(),
            'heading': CKEditorAdminWidget(),
            'conclusion': CKEditorAdminWidget(),
        }

    def clean_tags(self):

        super().clean()

        cleaned_tags = clean_tags(self)
        return cleaned_tags


class SubsectionAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'
        self.fields['title'].widget.attrs['placeholder'] = _('Enter title')

        self.fields['slug'].disabled = True
        self.fields['slug'].widget.attrs['class'] = 'span12'

    class Meta:
        model = Subsection
        fields = ('title', )
        widgets = {
            'content': CKEditorAdminWidget(),
        }
