
from django.utils.translation import ungettext_lazy
from django import forms

from .models import Solution, Tag, Question


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('title',)

    def clean(self):
        count_tags = len(self.cleaned_data.get('tags', '0'))
        if count_tags < Tag.MIN_COUNT_TAGS_ON_OBJECT:
            raise forms.ValidationError({
                'tags': ungettext_lazy(
                    'Solution must be have at least %(number)d tag',
                    'Solution must be have at least %(number)d tags',
                    'number',
                ) % {
                    'number': Tag.MIN_COUNT_TAGS_ON_OBJECT,
                }
            })
        if count_tags > Tag.MAX_COUNT_TAGS_ON_OBJECT:
            raise forms.ValidationError({
                'tags': ungettext_lazy(
                    'Solution must be have no more %(number)d tag',
                    'Solution must be have no more %(number)d tags',
                    'number',
                ) % {
                    'number': Tag.MAX_COUNT_TAGS_ON_OBJECT,
                }
            })


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title',)

    def clean(self):
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
