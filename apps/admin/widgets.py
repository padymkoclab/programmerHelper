
import copy

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


class RelatedFieldWidgetWrapper(forms.Widget):
    """docstring for RelatedFieldWidgetWrapper."""

    template = 'admin/admin/relatedfieldwidgetwrapper.html'

    def __init__(self, widget, db_field, site_admin, *args, **kwargs):
        self.db_field = db_field
        self.related_model = db_field.remote_field.model
        self.widget = widget
        self.attrs = widget.attrs
        self.site_admin = site_admin

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj
        return obj

    def render(self, name, value, attrs=None):

        attrs = {
            'class': 'form-control',
        }

        # Add permissions on actions
        add_url = self.site_admin.get_url('add', self.related_model._meta)

        context = {
            'rendered_widget': self.widget.render(name, value, attrs),
            'add_url': add_url,
        }

        if value:
            obj = self.related_model._default_manager.get(pk=value)

            update_url = self.site_admin.get_url('change', self.related_model._meta, kwargs={'pk': obj.pk})
            delete_url = self.site_admin.get_url('delete', self.related_model._meta, kwargs={'pk': obj.pk})

            context.update({
                'update_url': update_url,
                'delete_url': delete_url,
            })

        return template.loader.render_to_string(self.template, context)
