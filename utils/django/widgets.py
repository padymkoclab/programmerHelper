
import logging

from django import template
from django.forms.utils import flatatt
from django.utils.text import force_text
from django.contrib import postgres
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe, format_html
from django.contrib.admin.widgets import AdminFileWidget
from django import forms


logger = logging.getLogger('django.development')


class AdminImageThumbnail(AdminFileWidget):

    def render(self, name, value, attrs=None):

        # get a HTML output
        html = super().render(name, value, attrs)

        # if an object has image
        if value:
            img_styles = 'float: left; margin-right: 15px; width: 100px; height: 100px;'

            if isinstance(value, ImageFieldFile):
                return mark_safe(
                    '<image src="{0}" style="{1}"></image>{2}'.format(value.url, img_styles, html)
                )
        return html


class DurationSplitWidget(forms.MultiWidget):

    class Media:
        css = {
            'all': ('utils/css/durationsplitwidget.css', ),
        }

    def __init__(self):

        # attributes for a NumberInput of days
        days_attrs = {
            'min': 0,
            'value': 0,
        }

        # choices hours from 00 .. 23
        choices_hours = [(i, str(i).zfill(2))for i in range(24)]

        # choices minutes from 00 .. 59
        choices_minutes = [(i, str(i).zfill(2))for i in range(60)]

        # choices seconds from 00 .. 59
        choices_seconds = [(i, str(i).zfill(2))for i in range(60)]

        widgets = (
            forms.NumberInput(attrs=days_attrs),
            forms.Select(choices=choices_hours),
            forms.Select(choices=choices_minutes),
            forms.Select(choices=choices_seconds),
        )

        # raise super with widgets and without attrs
        super().__init__(widgets, {})

    def decompress(self, value):

        if value:
            count_days, str_time = value.split(' ')
            count_days = int(count_days)
            hours, minutes, seconds = map(int, str_time.split(':'))
            return [count_days, hours, minutes, seconds]
        else:
            return [0, 0, 0, 0]

    def format_output(self, rendered_widgets):

        # return as - days hours:minutes:seconds
        inputs_time = '&nbsp;:&nbsp;'.join(rendered_widgets[1:])
        return '{}&nbsp;{}'.format(rendered_widgets[0], inputs_time)

    def render(self, name, value, attrs=None):

        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')

        labels_texts = [_('Days'), _('Hours'), _('Minutes'), _('Seconds')]

        for i, label_text_and_widget in enumerate(zip(labels_texts, self.widgets)):

            label_text = label_text_and_widget[0]
            widget = label_text_and_widget[1]

            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))

            # add a label
            label_html = '<label for="{}">{}</label>'.format(final_attrs['id'], label_text)
            input_html = widget.render(name + '_%s' % i, widget_value, final_attrs)

            wrapper = '<div class="div_input_durationfield">{}{}</div>'.format(label_html, input_html)

            output.append(wrapper)
        return mark_safe(self.format_output(output))


class DurationWidget(forms.widgets.TextInput):

    class Media:
        css = {
            'all': ('utils/css/durationwidget.css', ),
        }
        js = ('utils/js/durationwidget.js', )

    def render(self, name, value, attrs=None):

        rendered_html = super().render(name, value, attrs)

        if value:
            if ' ' not in value:
                fullvalue = '0:' + value
            else:
                fullvalue = value.replace(' ', ':')
            self.days, self.hours, self.minutes, self.seconds = map(int, fullvalue.split(':'))
        else:
            self.days, self.hours, self.minutes, self.seconds = (0, 0, 0, 0)
        additional_markup = self.additional_markup()

        return mark_safe(rendered_html + additional_markup)

    def additional_markup(self):
        """ """

        return """
        <div class="div_input_ranges_durationfield">
            <table>
                <tbody>
                    <tr>
                        <td>{0}</td>
                        <td><input type="range" name="days" min=0 value="{1}"></td>
                    </tr>
                    <tr>
                        <td>{2}</td>
                        <td><input type="range" name="hours" min=0 max=23 value="{3}"></td>
                    </tr>
                    <tr>
                        <td>{4}</td>
                        <td><input type="range" name="minutes" min=0 max=59 value="{5}"></td>
                    </tr>
                    <tr>
                        <td>{6}</td>
                        <td><input type="range" name="seconds" min=0 max=59 value="{7}"></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """.format(
            _('Days'), self.days,
            _('Hours'), self.hours,
            _('Minutes'), self.minutes,
            _('Seconds'), self.seconds,
        )


class HorizontalRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        css_style = 'style="display: inline-block; margin-right: 10px;"'

        self.renderer.inner_html = '<li ' + css_style + '>{choice_value}{sub_widgets}</li>'


class BooleanRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = [(True, _('Yes')), (False, _('No'))]


class SplitInputsArrayWidget(postgres.forms.SplitArrayWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):

        value_from_datadict = super().value_from_datadict(data, files, name)

        # convert a list to a string, with commas-separated values
        value_from_datadict = ','.join(value_from_datadict)

        return value_from_datadict

    def render(self, name, value, attrs=None):

        # if object has value, then
        # convert a sting to a list by commas between values
        if value is not None:
            value = value.split(',')

        return super().render(name, value, attrs=None)


class ColorInput(forms.Widget):
    """
    Bootstrap Color widget
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """

    class Media:
        css = {
            'all': ('utils/css/colorwidget.css', ),
        }
        js = ('utils/js/colorwidget.js', )

    def format_value(self, value):
        return value

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''

        final_attrs = self.build_attrs(
            attrs,
            **{
                'type': 'text',
                'name': name,
                'readonly': True,
                'class': 'form-control',
            }
        )

        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))

        html_ = """
        <div class="colorfield input-group">
            <span class="input-group-addon">
                <input type="color" name="color_input" value="{}" />
            </span>
            <input{} />
        </div>
        """

        return format_html(html_, value, flatatt(final_attrs))


class AutosizedTextarea(forms.Textarea):

    class Media:
        js = ('utils/js/autoresize.js', )

    def render(self, name, value, attrs=None):

        output = super().render(name, value, attrs)

        output += "<script>$('#{}').AutoResize();</script>".format(attrs['id'])

        return output


class ReadOnlyWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        return value


class DateTimeWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        css_class = 'datetime_widget'
        input_id = attrs['id']
        attrs['class'] = 'form-control {}'.format(css_class)
        output = super(DateTimeWidget, self).render(name, value, attrs)

        output += "<script type='text/javascript'>$('input#{}.{}').datepicker();</script>".format(input_id, css_class)
        return output


class TextInputFixed(forms.TextInput):

    def __init__(self, *args, **kwargs):
        super(TextInputFixed, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):

        output = super(TextInputFixed, self).render(name, value, attrs)
        startswith = self.modelfield.startswith

        output = """
        <div class="input-group">
            <span class="input-group-addon">{}</span>
             {}
        </div>
        """.format(startswith, output)

        return mark_safe(output)


class CKEditorWidget(forms.Textarea):

    class Media:
        js = ('vendor/ckeditor/ckeditor.js', )

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        attrs = forms.utils.flatatt(final_attrs)

        element_id = final_attrs['id']

        return format_html(
            '<textarea{}>\r\n{}</textarea><script>CKEDITOR.replace("{}")</script>',
            attrs, force_text(value), element_id
        )


class TinyMCEWidget(forms.Textarea):

    class Media:
        js = ('vendor/tinymce/tinymce.min.js', )

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        attrs = forms.utils.flatatt(final_attrs)

        element_id = final_attrs['id']

        html_ = """
        <textarea{}>\r\n{}</textarea>
        <script>
            var options = new Object;
            options.selector = "#{}";
            tinymce.init(options);
        </script>""".format(
            attrs, force_text(value), element_id
        )
        return mark_safe(html_)
