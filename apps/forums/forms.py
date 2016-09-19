
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from suit.widgets import AutosizedTextarea

from utils.django.widgets import AdminImageThumbnail

from .models import Section, Forum, Topic, Post


logger = logging.getLogger('django.development')


class SectionAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['position'].widget.attrs['class'] = 'span2'
        self.fields['position'].widget.attrs['min'] = 1

        logger.error('Displayed TextInput istead of NumberInput for field "Section.position"')

    class Meta:
        model = Section
        fields = ('name', 'groups', 'position', 'image')
        widgets = {
            'image': AdminImageThumbnail(),
        }


class ForumInlineAdminModelForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ('name', )


class FormAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'span12'
        self.fields['name'].widget.attrs['placeholder'] = _('Enter name')

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['section'].widget.widget.attrs['class'] = 'span11'

    class Meta:
        model = Forum
        fields = ('name', )
        widgets = {
            'description': AutosizedTextarea(attrs={
                'placeholder': _('Enter description'),
                'class': 'span12',
            })
        }


class TopicAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs['class'] = 'span12'
        self.fields['subject'].widget.attrs['placeholder'] = _('Enter subject')

        self.fields['slug'].widget.attrs['class'] = 'span12'
        self.fields['slug'].disabled = True

        self.fields['forum'].widget.widget.attrs['class'] = 'span11'


class PostAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        # admin inline has not field topic
        if 'topic' in self.fields:
            self.fields['topic'].widget.widget.attrs['class'] = 'span11'

        self.fields['markup'].widget.attrs['class'] = 'span3'

        self.fields['content'].widget.attrs['placeholder'] = _('Enter text according to the selected markup')
        self.fields['content'].widget.attrs['class'] = 'span12'
        self.fields['content'].widget.attrs['rows'] = 10

        self.fields['user_ip'].widget.attrs['class'] = 'span5'
        self.fields['user_ip'].disabled = True
