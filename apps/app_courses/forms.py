
from collections import Counter

from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name',)

    def clean(self):
        super(CourseForm, self).clean()
        authorship = self.cleaned_data.get('authorship', None)
        if authorship is not None:
            count_authors = len(authorship)
            if count_authors > Course.MAX_COUNT_AUTHORS:
                error_message = _('Sorry, but count authors not possible more than {0}. Now {1}.'.format(
                    Course.MAX_COUNT_AUTHORS,
                    count_authors,
                ))
                raise forms.ValidationError({
                    'authorship': error_message,
                })


class LessonInlineFormSet(forms.BaseInlineFormSet):
    """
    Special inline form for relationship between TestQuestion and Varian models.
    """

    def clean(self):
        """Validation what must unique numbers of lessons in formset."""
        super(LessonInlineFormSet, self).clean()
        all_numbers_of_lessons = list()
        for form in self.forms:
            number = form.cleaned_data.get('number', None)
            all_numbers_of_lessons.append(number)
        t = list()
        for key, value in Counter(all_numbers_of_lessons).items():
            if value > 1:
                t.append(key)
        for form in self.forms:
            number = form.cleaned_data.get('number', None)
            if number in t:
                form.add_error('number', _('Please don`t repeat your number.'))


class SublessonInlineFormSet(forms.BaseInlineFormSet):
    """
    Special inline form for relationship between TestQuestion and Varian models.
    """

    def clean(self):
        """Validation what must unique numbers of lessons in formset."""
        super(SublessonInlineFormSet, self).clean()
        all_numbers_of_sublessons = list()
        for form in self.forms:
            number = form.cleaned_data.get('number', None)
            all_numbers_of_sublessons.append(number)
        t = list()
        for key, value in Counter(all_numbers_of_sublessons).items():
            if value > 1:
                t.append(key)
        for form in self.forms:
            number = form.cleaned_data.get('number', None)
            if number in t:
                form.add_error('number', _('Please don`t repeat your number.'))
        # import pdb; pdb.set_trace()
