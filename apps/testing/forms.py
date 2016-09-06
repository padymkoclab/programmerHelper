
from django import forms

from suit.widgets import AutosizedTextarea

from mylabour.widgets import AdminImageThumbnail, DurationWidget
# from mylabour.forms_fields import DurationSplitField

from .models import Suit, TestQuestion, Variant


class VariantAdminModelForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ('text_variant', 'question', 'is_right_variant')

    def __init__(self, *args, **kwargs):
        super(VariantAdminModelForm, self).__init__(*args, **kwargs)

        self.fields['question'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_variant'].widget = AutosizedTextarea(attrs={'class': 'span12'})


class TestQuestionAdminModelForm(forms.ModelForm):

    class Meta:
        model = TestQuestion
        fields = ['title', 'suit', 'text_question', 'slug']

    def __init__(self, *args, **kwargs):
        super(TestQuestionAdminModelForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['suit'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_question'].widget = AutosizedTextarea(attrs={'class': 'span12'})


class TestQuestionAdminInlineModelForm(forms.ModelForm):

    class Meta:
        model = TestQuestion
        fields = ['title', 'suit', 'text_question', 'slug']

    def __init__(self, *args, **kwargs):
        super(TestQuestionAdminInlineModelForm, self).__init__(*args, **kwargs)

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

        self.fields['status'].widget.attrs['class'] = 'span12'

        self.fields['duration'].widget = DurationWidget(attrs={'class': 'span2'})

        self.fields['complexity'].widget.attrs['class'] = 'span12'

        self.fields['description'].widget = AutosizedTextarea(attrs={'class': 'span12'})
