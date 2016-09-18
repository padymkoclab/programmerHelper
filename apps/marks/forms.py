
from django import forms

from .models import Mark


class MarkAdminModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.widget.attrs['class'] = 'span10'

        mark_field = self.fields['mark']
        mark_choices = [(i, i) for i in range(Mark.MIN_MARK, Mark.MAX_MARK + 1)]
        mark_field.widget = forms.Select(
            choices=mark_choices, attrs={'class': 'span9'}
        )

    class Meta:
        model = Mark
        fields = ('user', 'mark')
