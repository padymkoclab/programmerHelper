
from django import forms

from apps.tags.forms import clean_tags

from .models import Solution, Category


class CategoryForm(forms.ModelForm):
    """
    ModelForm for Category.
    """

    class Meta:
        model = Category
        fields = ('name', 'slug', 'description')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['slug'].disabled = True


class SolutionForm(forms.ModelForm):
    """
    ModelForm for Solution.
    """

    class Meta:
        model = Solution
        fields = ('tags', 'links', 'slug')

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)
        self.fields['slug'].disabled = True

    def clean_tags(self):
        super(SolutionForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags
