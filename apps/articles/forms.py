
import collections

from django.utils.translation import ugettext_lazy as _
from django import forms

from apps.tags.forms import clean_tags

from .models import Article, ArticleSubsection


class ArticleForm(forms.ModelForm):
    """

    """

    class Meta:
        model = Article
        fields = ('tags', 'links', 'slug')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['slug'].disabled = True

    def clean_tags(self):
        super(ArticleForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags


class ArticleSubsectionFormset(forms.models.BaseInlineFormSet):
    """

    """

    slug = forms.CharField(disabled=True)

    class Meta:
        model = ArticleSubsection
        fields = ('number', )
        widgets = {
            'slug': forms.Textarea(attrs={'disabled': True}),
        }

    def add_fields(self, form, index):
        super(ArticleSubsectionFormset, self).add_fields(form, index)
        form.fields['slug'].disabled = True

    def clean(self):
        super(ArticleSubsectionFormset, self).clean()
        # validate unique number of subarticle on formset
        counter_numbers_of_subsections = collections.Counter(
            form.cleaned_data.get('number', None) for form in self.forms
        )
        for form in self.forms:
            number = form.cleaned_data.get('number', None)
            if counter_numbers_of_subsections.get(number, 0) > 1:
                form.add_error('__all__', _('Number of subsection "{0}" is repeated.').format(number))
        # validate unique title of subarticle with article (considering AutoSlugField)
        counter_titles_of_subsections = collections.Counter(form.cleaned_data.get('title', None) for form in self.forms)
        for form in self.forms:
            title = form.cleaned_data.get('title', None)
            if counter_titles_of_subsections.get(title, 0) > 1:
                form.add_error('__all__', _('Title of subsection "{0}" is repeated.').format(title))
