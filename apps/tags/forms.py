
from django import forms
from django.utils.translation import ugettext_lazy as _

from suit.widgets import AutosizedTextarea

from .models import Tag


def clean_tags(form_instance):
    """ """

    tags = form_instance.cleaned_data['tags']
    if not Tag.MIN_COUNT_TAGS_ON_OBJECT <= len(tags) <= Tag.MAX_COUNT_TAGS_ON_OBJECT:
        msg = _('{0} may has from {1} to {2} tags.').format(
            form_instance.Meta.model._meta.verbose_name,
            Tag.MIN_COUNT_TAGS_ON_OBJECT,
            Tag.MAX_COUNT_TAGS_ON_OBJECT,
        )
        form_instance.add_error('tags', msg)
    return tags


class TagAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['description'].widget = AutosizedTextarea(attrs={
            'class': 'span12',
            'placeholder': _('Enter description'),
        })
