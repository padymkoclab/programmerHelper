
from django import forms

from suit_ckeditor.widgets import CKEditorWidget

from utils.django.forms_utils import BooleanRadioSelect

from apps.tags.forms import clean_tags

from .models import Question, Answer


class QuestionAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span12'

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_question'].widget = CKEditorWidget()

    class Meta:
        model = Question
        fields = ('title', 'slug')
        widgets = {
            'status': forms.RadioSelect()
        }

    def clean(self):
        super().clean()

        clean_tags(self)


class AnswerAdminModelForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('text_answer', )
        widgets = {
            'is_accepted': BooleanRadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        self.fields['question'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_answer'].widget = CKEditorWidget()


class AnswerInlineAdminModelForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('text_answer', )
        widgets = {
            'is_accepted': BooleanRadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        self.fields['text_answer'].widget = CKEditorWidget()
