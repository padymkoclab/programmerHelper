
from django.utils.translation import ungettext_lazy
from django import forms

from .models import Question, Tag


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title',)

    def clean(self):
        super(QuestionForm, self).clean()
        count_tags = len(self.cleaned_data.get('tags', '0'))
        if count_tags < Tag.MIN_COUNT_TAGS_ON_OBJECT:
            raise forms.ValidationError({
                'tags': ungettext_lazy(
                    'Question must be have at least %(number)d tag',
                    'Question must be have at least %(number)d tags',
                    'number',
                ) % {
                    'number': Tag.MIN_COUNT_TAGS_ON_OBJECT,
                }
            })
        if count_tags > Tag.MAX_COUNT_TAGS_ON_OBJECT:
            raise forms.ValidationError({
                'tags': ungettext_lazy(
                    'Question must be have no more %(number)d tag',
                    'Question must be have no more %(number)d tags',
                    'number',
                ) % {
                    'number': Tag.MAX_COUNT_TAGS_ON_OBJECT,
                }
            })
