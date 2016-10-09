
from django import forms
from django import template
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class BootstrapFileInput(forms.widgets.FileInput):

    def get_fileinput(self, name, value, attrs=None):

        if attrs is None:
            attrs = dict()

        attrs['style'] = 'display: none;'

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))

        return format_html('<input{} />', flatatt(final_attrs))

    def render(self, name, value, attrs=None):

        fileinput = self.get_fileinput(name, value, attrs)
        return fileinput
