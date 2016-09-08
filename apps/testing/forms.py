
from django import forms

from suit.widgets import AutosizedTextarea

from utils.django.widgets import AdminImageThumbnail, DurationWidget

from .models import Suit, Question, Variant


class VariantAdminModelForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ('text_variant', 'question', 'is_right_variant')

    def __init__(self, *args, **kwargs):
        super(VariantAdminModelForm, self).__init__(*args, **kwargs)

        self.fields['question'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_variant'].widget = AutosizedTextarea(attrs={'class': 'span12'})


class QuestionAdminModelForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'suit', 'text_question', 'slug']

    def __init__(self, *args, **kwargs):
        super(QuestionAdminModelForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['suit'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_question'].widget = AutosizedTextarea(attrs={'class': 'span12'})


class QuestionAdminInlineModelForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'suit', 'text_question', 'slug']

    def __init__(self, *args, **kwargs):
        super(QuestionAdminInlineModelForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['text_question'].widget = AutosizedTextarea(attrs={'class': 'span12'})


class SuitAdminModelForm(forms.ModelForm):

    class Meta:
        model = Suit
        fields = ['name', 'slug', 'duration', 'status', 'description', 'complexity']

    def __init__(self, *args, **kwargs):

        super(SuitAdminModelForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['image'].widget = AdminImageThumbnail()

        self.fields['duration'].widget = DurationWidget(attrs={'class': 'span2'})
        self.fields['duration'].disabled = True

        self.fields['complexity'].widget.attrs['class'] = 'span12'

        self.fields['description'].widget = AutosizedTextarea(attrs={'class': 'span12'})
