
from django.utils.translation import ugettext_lazy as _
from django import forms

from suit.widgets import AutosizedTextarea

from utils.django.widgets import HorizontalRadioSelect

from .models import Reply


HorizontalRadioSelectMarks = HorizontalRadioSelect(
    choices=tuple((n, n)for n in range(Reply.MIN_MARK, Reply.MAX_MARK + 1))
)


class ReplyAdminModelForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('user', )
        widgets = {
            'mark_for_style': HorizontalRadioSelectMarks,
            'mark_for_content': HorizontalRadioSelectMarks,
            'mark_for_language': HorizontalRadioSelectMarks,
            'text_reply': AutosizedTextarea(attrs={
                'placeholder': _('Enter text'),
                'class': 'span12',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span11'

        self.fields['advantages'].widget.attrs['class'] = 'span12'
        self.fields['advantages'].widget.attrs['placeholder'] = _('Enter words')

        self.fields['disadvantages'].widget.attrs['class'] = 'span12'
        self.fields['disadvantages'].widget.attrs['placeholder'] = _('Enter words')
