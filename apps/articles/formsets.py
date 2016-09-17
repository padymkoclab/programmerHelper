
import collections

from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Subsection


class SubsectionFormset(forms.models.BaseInlineFormSet):
    """

    """

    slug = forms.CharField(disabled=True)

    class Meta:
        model = Subsection
        fields = ('number', )
        widgets = {
            'slug': forms.Textarea(attrs={'disabled': True}),
        }

    def clean(self):

        super().clean()
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
