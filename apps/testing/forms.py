
from django.utils.translation import ugettext_lazy as _
from django import forms

# from suit.widgets import AutosizedTextarea

from utils.django.widgets import AdminImageThumbnail, DurationWidget

from .models import Suit, Question, Variant


class SuitAdminModelForm(forms.ModelForm):

    class Meta:
        model = Suit
        fields = ['name', 'slug', 'duration', 'status', 'description', 'complexity']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['image'].widget = AdminImageThumbnail()

        self.fields['duration'].widget = DurationWidget(attrs={'class': 'span2'})
        self.fields['duration'].disabled = True

        self.fields['complexity'].widget.attrs['class'] = 'span12'

        # self.fields['description'].widget = AutosizedTextarea(attrs={
        #     'class': 'span12',
        #     'placeholder': _('Enter description')
        # })


class QuestionAdminModelForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'suit', 'text_question', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'
        self.fields['title'].widget.attrs['placeholder'] = _('Enter title')

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['suit'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_question'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter text of question')
        })


class QuestionAdminInlineModelForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'suit', 'text_question', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'
        self.fields['title'].widget.attrs['placeholder'] = _('Enter title')

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['text_question'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter text of question')
        })


class VariantAdminModelForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ('text_variant', 'question', 'is_right_variant')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['question'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_variant'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter text of variant')
        })
